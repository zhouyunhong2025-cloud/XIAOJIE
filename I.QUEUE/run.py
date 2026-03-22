#!/usr/bin/env python3
"""
🤖 I.QUEUE 完整启动器
同时启动 Web 服务器 + 桌面监控面板
"""

import sys
import subprocess
import time
import os
from pathlib import Path


def main():
    """启动主函数"""
    
    print("\n" + "="*70)
    print("🤖 I.QUEUE Agent 设计 & 执行系统")
    print("="*70)
    print("\n启动方式选择:\n")
    
    print("1️⃣  完整模式 (Web + 桌面监控)")
    print("   → 在浏览器设计 Agent")
    print("   → 在桌面面板监控执行")
    print()
    
    print("2️⃣  仅 Web 模式 (浏览器)")
    print("   → 访问 http://localhost:8000")
    print()
    
    print("3️⃣  仅 CLI 模式 (命令行)")
    print("   → python quick_start.py '你的需求'")
    print()
    
    choice = input("请选择 (1/2/3): ").strip()
    
    if choice == "1":
        start_full_mode()
    elif choice == "2":
        start_web_only()
    elif choice == "3":
        print("\n✅ 使用 CLI 模式:")
        print("   cd /path/to/I.QUEUE")
        print("   python quick_start.py '你的需求'\n")
    else:
        print("❌ 无效选择")
        sys.exit(1)


def start_full_mode():
    """完整模式：Web + 监控面板"""
    
    print("\n" + "="*70)
    print("启动: 完整模式 (Web + 桌面监控)")
    print("="*70 + "\n")
    
    # 获取项目路径
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    # 检查依赖
    print("📦 检查依赖...")
    try:
        import fastapi
        import uvicorn
        print("  ✓ FastAPI/Uvicorn")
    except ImportError:
        print("  ⚠️  缺少 FastAPI")
        print("  运行: pip install fastapi uvicorn")
        sys.exit(1)
    
    try:
        from PyQt6.QtWidgets import QApplication
        print("  ✓ PyQt6")
    except ImportError:
        print("  ⚠️  缺少 PyQt6")
        print("  运行: pip install PyQt6")
        sys.exit(1)
    
    print("\n")
    
    # 启动 Web 服务器（后台）
    print("🌐 启动 Web 服务器...")
    web_process = subprocess.Popen(
        [sys.executable, "web_server.py"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    print("   ✓ Web 服务器启动中...")
    
    # 等待 Web 服务器准备好
    time.sleep(2)
    
    print("   ✓ Web 服务器运行在 http://localhost:8000")
    print()
    
    # 启动桌面监控面板
    print("🖥️  启动桌面监控面板...")
    try:
        subprocess.run([sys.executable, "agent_monitor.py"])
    except KeyboardInterrupt:
        print("\n\n正在关闭...")
        web_process.terminate()
        web_process.wait(timeout=5)
    except Exception as e:
        print(f"❌ 启动监控面板失败: {e}")
        web_process.terminate()
        sys.exit(1)
    
    # 清理
    print("\n✅ I.QUEUE 已关闭")


def start_web_only():
    """仅 Web 模式"""
    
    print("\n" + "="*70)
    print("启动: Web 模式")
    print("="*70)
    print("\n🌐 Web 服务器启动中...")
    print("   🔗 访问: http://localhost:8000")
    print("   📖 文档: http://localhost:8000/docs")
    print("\n按 Ctrl+C 停止服务器\n")
    
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    try:
        subprocess.run([sys.executable, "web_server.py"])
    except KeyboardInterrupt:
        print("\n✅ Web 服务器已关闭")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 再见!")
        sys.exit(0)
