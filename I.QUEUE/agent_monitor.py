"""
I.QUEUE 运行监控面板 - 桌面应用
悬浮在系统桌面上，实时显示 Agent 执行状态
"""

import sys
import threading
import json
from datetime import datetime
from pathlib import Path
from collections import deque

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTextEdit, QPushButton, QProgressBar, QTabWidget,
    QTableWidget, QTableWidgetItem, QScrollArea, QFrame
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QObject, QThread
from PyQt6.QtGui import QFont, QColor, QIcon, QTextCursor
from PyQt6.QtCore import QSize
import requests
from typing import Optional


class WorkerSignals(QObject):
    """Worker 信号"""
    update_status = pyqtSignal(str, str)  # status, message
    update_log = pyqtSignal(str)          # log line
    deployment_started = pyqtSignal(str)  # requirement
    deployment_finished = pyqtSignal(bool)  # success


class MonitorWorker(QThread):
    """后台监控线程"""
    
    signals = WorkerSignals()
    
    def __init__(self):
        super().__init__()
        self.running = True
        self.api_endpoint = "http://localhost:8000/api"
        self.logs = deque(maxlen=1000)
        
    def run(self):
        """监控主循环"""
        self.signals.update_status.emit("就绪", "监控系统启动")
        
        while self.running:
            try:
                # 检查 API 状态
                response = requests.get(f"{self.api_endpoint.replace('/api', '')}/health", timeout=2)
                if response.status_code == 200:
                    self.signals.update_status.emit("在线", "✅ API 服务正常")
                else:
                    self.signals.update_status.emit("离线", "❌ API 连接异常")
            except:
                self.signals.update_status.emit("离线", "❌ 无法连接 API")
            
            self.msleep(1000)  # 每 1 秒检查一次
    
    def stop(self):
        """停止监控"""
        self.running = False


class AgentMonitorUI(QMainWindow):
    """Agent 运行监控 UI"""
    
    def __init__(self):
        super().__init__()
        self.current_plan = None
        self.execution_logs = deque(maxlen=500)
        
        # 窗口设置
        self.setWindowTitle("🤖 I.QUEUE Agent 运行监控")
        self.setGeometry(1500, 100, 500, 700)  # 靠右侧悬浮
        self.setWindowFlags(
            Qt.WindowType.Window |
            Qt.WindowType.WindowStaysOnTopHint |  # 始终在最上面
            Qt.WindowType.FramelessWindowHint
        )
        
        # 创建 UI
        self.init_ui()
        
        # 启动后台监控
        self.monitor_worker = MonitorWorker()
        self.monitor_worker.signals.update_status.connect(self.update_status)
        self.monitor_worker.signals.update_log.connect(self.add_log)
        self.monitor_worker.start()
        
        # 应用样式
        self.apply_styles()
        
        # 显示窗口
        self.show()
    
    def init_ui(self):
        """初始化用户界面"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # ===== 顶部：状态栏 =====
        header = self.create_header()
        main_layout.addWidget(header)
        
        # ===== 中部：标签页 =====
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabBar::tab {
                padding: 8px 16px;
                background: #334155;
                color: #f1f5f9;
                border: none;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: #2563eb;
                color: white;
            }
        """)
        
        # Tab 1: 实时日志
        self.log_widget = QTextEdit()
        self.log_widget.setReadOnly(True)
        self.log_widget.setFont(QFont("Courier", 9))
        tabs.addTab(self.log_widget, "📋 实时日志")
        
        # Tab 2: 执行统计
        stats_widget = self.create_stats_widget()
        tabs.addTab(stats_widget, "📊 执行统计")
        
        # Tab 3: 快速操作
        actions_widget = self.create_actions_widget()
        tabs.addTab(actions_widget, "⚙️ 快速操作")
        
        main_layout.addWidget(tabs)
        
        # ===== 底部：控制栏 =====
        footer = self.create_footer()
        main_layout.addWidget(footer)
    
    def create_header(self):
        """创建顶部状态栏"""
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background: linear-gradient(90deg, #1e293b 0%, #0f172a 100%);
                border-bottom: 2px solid #2563eb;
                padding: 12px;
            }
        """)
        
        layout = QVBoxLayout(header)
        layout.setSpacing(8)
        layout.setContentsMargins(12, 8, 12, 8)
        
        # 标题
        title = QLabel("🤖 I.QUEUE Agent 监控")
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        title.setStyleSheet("color: #3b82f6;")
        layout.addWidget(title)
        
        # 状态行
        status_layout = QHBoxLayout()
        
        self.status_indicator = QLabel("◉")
        self.status_indicator.setStyleSheet("color: #ef4444; font-size: 16px;")
        status_layout.addWidget(self.status_indicator)
        
        self.status_text = QLabel("连接中...")
        self.status_text.setStyleSheet("color: #cbd5e1;")
        status_layout.addWidget(self.status_text)
        
        status_layout.addStretch()
        layout.addLayout(status_layout)
        
        # 进度条
        self.progress = QProgressBar()
        self.progress.setStyleSheet("""
            QProgressBar {
                border: none;
                background: #334155;
                border-radius: 4px;
                height: 6px;
            }
            QProgressBar::chunk {
                background: linear-gradient(90deg, #3b82f6, #8b5cf6);
                border-radius: 4px;
            }
        """)
        self.progress.setMaximum(100)
        self.progress.setValue(0)
        layout.addWidget(self.progress)
        
        return header
    
    def create_stats_widget(self):
        """创建统计信息面板"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)
        
        stats = [
            ("🚀 已部署 Agent", "0", "#10b981"),
            ("✅ 成功执行", "0", "#10b981"),
            ("⏱️ 平均响应", "0ms", "#3b82f6"),
            ("📊 总处理数", "0", "#f59e0b"),
        ]
        
        self.stat_labels = {}
        
        for icon, key, color in stats:
            h_layout = QHBoxLayout()
            
            label = QLabel(icon)
            label.setStyleSheet(f"color: {color}; font-size: 14px;")
            h_layout.addWidget(label)
            
            value = QLabel()
            value.setStyleSheet(f"color: #f1f5f9; font-weight: bold;")
            self.stat_labels[key] = value
            h_layout.addWidget(value)
            
            h_layout.addStretch()
            layout.addLayout(h_layout)
        
        layout.addStretch()
        return widget
    
    def create_actions_widget(self):
        """创建快速操作面板"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)
        
        # 按钮列表
        buttons = [
            ("🌐 打开 Web 界面", self.open_web_ui),
            ("📂 打开输出文件夹", self.open_output_folder),
            ("🔄 刷新状态", self.refresh_status),
            ("📋 导出日志", self.export_logs),
            ("⚠️ 清空日志", self.clear_logs),
        ]
        
        for text, callback in buttons:
            btn = QPushButton(text)
            btn.setStyleSheet("""
                QPushButton {
                    background: #2563eb;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 10px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: #1d4ed8;
                }
                QPushButton:pressed {
                    background: #1e40af;
                }
            """)
            btn.clicked.connect(callback)
            layout.addWidget(btn)
        
        layout.addStretch()
        return widget
    
    def create_footer(self):
        """创建底部控制栏"""
        footer = QFrame()
        footer.setStyleSheet("""
            QFrame {
                background: #1e293b;
                border-top: 1px solid #475569;
                padding: 8px 12px;
            }
        """)
        
        layout = QHBoxLayout(footer)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(8)
        
        # 时间显示
        self.time_label = QLabel()
        self.time_label.setStyleSheet("color: #94a3b8; font-size: 10px;")
        layout.addWidget(self.time_label)
        
        layout.addStretch()
        
        # 版本
        version = QLabel("v2.0 • PyQt6")
        version.setStyleSheet("color: #94a3b8; font-size: 10px;")
        layout.addWidget(version)
        
        # 更新时间
        self.update_time_timer = QTimer()
        self.update_time_timer.timeout.connect(self.update_time)
        self.update_time_timer.start(1000)
        
        return footer
    
    def update_status(self, status: str, message: str):
        """更新状态"""
        color_map = {
            "在线": "#10b981",
            "离线": "#ef4444",
            "就绪": "#3b82f6",
        }
        
        color = color_map.get(status, "#94a3b8")
        self.status_indicator.setStyleSheet(f"color: {color}; font-size: 16px;")
        self.status_text.setText(message)
        
        self.add_log(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
    
    def add_log(self, message: str):
        """添加日志"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_line = f"[{timestamp}] {message}"
        
        self.execution_logs.append(log_line)
        
        # 添加到日志显示
        cursor = self.log_widget.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.log_widget.setTextCursor(cursor)
        self.log_widget.insertPlainText(log_line + "\n")
        
        # 自动滚动到底
        cursor = self.log_widget.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.log_widget.setTextCursor(cursor)
    
    def update_time(self):
        """更新时间显示"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.setText(f"⏰ {current_time}")
    
    def open_web_ui(self):
        """打开 Web UI"""
        import webbrowser
        webbrowser.open("http://localhost:8000")
        self.add_log("✓ 已打开 Web 界面")
    
    def open_output_folder(self):
        """打开输出文件夹"""
        import subprocess
        output_dir = "/workspaces/XIAOJIE/I.QUEUE/mnt/user-data/outputs"
        try:
            subprocess.Popen(["xdg-open", output_dir])
            self.add_log(f"✓ 已打开输出文件夹: {output_dir}")
        except:
            self.add_log(f"❌ 无法打开文件夹")
    
    def refresh_status(self):
        """刷新状态"""
        self.add_log("🔄 正在刷新系统状态...")
        # 触发监控刷新
    
    def export_logs(self):
        """导出日志"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f"/tmp/i_queue_logs_{timestamp}.txt"
        
        try:
            with open(log_file, "w", encoding="utf-8") as f:
                f.write("\n".join(self.execution_logs))
            self.add_log(f"✓ 日志已导出: {log_file}")
        except Exception as e:
            self.add_log(f"❌ 导出失败: {str(e)}")
    
    def clear_logs(self):
        """清空日志"""
        self.log_widget.clear()
        self.execution_logs.clear()
        self.add_log("🗑️ 日志已清空")
    
    def apply_styles(self):
        """应用全局样式"""
        style = """
            QMainWindow {
                background: #0f172a;
                color: #f1f5f9;
            }
            QWidget {
                background: #0f172a;
                color: #f1f5f9;
            }
            QTextEdit {
                background: #1e293b;
                color: #cbd5e1;
                border: 1px solid #334155;
                border-radius: 4px;
                padding: 8px;
                font-family: "Courier New";
            }
            QLabel {
                color: #f1f5f9;
            }
            QTabWidget::pane {
                border: 1px solid #334155;
            }
        """
        self.setStyleSheet(style)
    
    def closeEvent(self, event):
        """关闭事件"""
        self.monitor_worker.stop()
        self.monitor_worker.wait()
        event.accept()


def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 设置应用样式
    app.setStyle("Fusion")
    
    # 创建并显示监控面板
    monitor = AgentMonitorUI()
    monitor.add_log("=== I.QUEUE Agent 监控面板已启动 ===")
    monitor.add_log("✓ 监控系统就绪")
    monitor.add_log("💡 提示: 打开 Web 界面 → 输入需求 → 一键启动")
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
