# 🚀 I.QUEUE 启动指南

## 三种启动方式

### 方式 1️⃣: 完整模式 (推荐)

**Web 界面 + 桌面监控面板 + 一键启动**

```bash
cd I.QUEUE
python run.py
# 选择: 1️⃣ 完整模式
```

**你会看到:**
1. 🌐 Web 浏览器打开设计界面 (http://localhost:8000)
2. 🖥️ 桌面悬浮监控面板
   - 📋 实时日志显示
   - 📊 执行统计
   - ⚙️ 快速操作

**工作流:**
```
输入需求
  ↓
点击"智能分析"
  ↓
查看设计报告
  ↓
点击"一键启动"
  ↓
监控面板实时显示执行日志 ✨
```

---

### 方式 2️⃣: 仅 Web 模式

**只使用浏览器，不需要桌面应用**

```bash
cd I.QUEUE
python web_server.py
```

**访问:**
- 🌐 Web UI: http://localhost:8000
- 📚 API 文档: http://localhost:8000/docs

---

### 方式 3️⃣: 仅 CLI 模式

**命令行快速使用**

```bash
cd I.QUEUE
python quick_start.py "你的需求"
```

**示例:**
```bash
python quick_start.py "帮我总结今天的工作"
# 自动生成: agent_plan_YYYYMMDD_HHMMSS.md + 配置文件
```

---

## 安装依赖

```bash
# 标准安装 (包含所有功能)
pip install -r requirements.txt

# 最小安装 (仅 Web)
pip install fastapi uvicorn requests

# 完整安装 (包含桌面应用)
pip install -r requirements.txt
pip install PyQt6
```

---

## 桌面监控面板详解

### 功能面板

| 标签 | 功能 | 用途 |
|-----|------|------|
| 📋 实时日志 | 显示系统日志 | 了解执行过程 |
| 📊 执行统计 | 性能指标 | 查看统计数据 |
| ⚙️ 快速操作 | 常用操作按钮 | 控制系统 |

### 快速操作按钮

```
🌐 打开 Web 界面
   → 打开设计器

📂 打开输出文件夹  
   → 查看生成的文件

🔄 刷新状态
   → 更新系统状态

📋 导出日志
   → 保存执行日志

⚠️ 清空日志
   → 清除日志文件
```

### 监控窗口位置

```
屏幕右侧悬浮
(500px 宽 × 700px 高)

始终在最上层
━━━━━━━━━━━━━━━━━━━━
│  🤖 I.QUEUE 监控    │
│                    │
│  状态: ✅ 在线     │
│  [进度条]           │
│                    │
│  📋 实时日志        │
│  系统日志输出       │
│  ...               │
│                    │
│  [按钮组]          │
━━━━━━━━━━━━━━━━━━━━
```

---

## 问题排查

### Q: 无法连接到 http://localhost:8000

**解决**:
```bash
# 检查端口是否被占用
lsof -i :8000

# 如果被占用，改用其他端口
python -m uvicorn web_server:app --port 8001
```

### Q: PyQt6 安装失败

**解决**:
```bash
# Ubuntu/Debian
sudo apt-get install python3-pyqt6

# macOS
brew install python-pyqt6

# 或使用 pip
pip install PyQt6 --upgrade
```

### Q: API 连接异常

**解决**:
1. 确保 Web 服务器正在运行
2. 检查防火墙设置
3. 查看日志调试

### Q: 监控面板无日志输出

**解决**:
1. 检查 API 是否正常
2. 在监控面板点击 "刷新状态"
3. 重启应用

---

## 高级用法

### 自定义端口

```bash
# 启动 Web 服务器在端口 9000
python -m uvicorn web_server:app --host 0.0.0.0 --port 9000
```

### 远程访问

```bash
# 允许其他计算机连接
python -m uvicorn web_server:app --host 0.0.0.0 --port 8000
# 其他计算机访问: http://your-ip:8000
```

### 后台运行

```bash
# Linux/macOS
nohup python web_server.py > server.log 2>&1 &

# 使用 screen
screen -S i_queue
python web_server.py
# Ctrl+A, D 退出

# 使用 tmux
tmux new-session -d -s i_queue
tmux send-keys -t i_queue "python web_server.py" Enter
```

---

## 快捷键和技巧

### Web 界面

| 快捷键 | 功能 |
|-------|------|
| Ctrl+Enter | 提交需求分析 |
| 拖拽 | 选择设计组件 |

### 监控面板

| 快捷键 | 功能 |
|-------|------|
| Ctrl+C | 关闭应用 |
| 按钮 | 快速操作 |

---

## 性能建议

### 系统要求
- **最低**: Python 3.9+, 4GB RAM, 50MB 磁盘空间
- **推荐**: Python 3.10+, 8GB RAM, 100MB 磁盘空间

### 优化建议
1. **关闭不用的标签页** 减少内存占用
2. **定期导出日志** 清空实时日志
3. **清理输出文件夹** (~mnt/user-data/outputs)
4. **更新依赖** `pip install -r requirements.txt --upgrade`

---

## 日志位置

```
📂 生成的文件:
   /workspaces/XIAOJIE/I.QUEUE/mnt/user-data/outputs/
   ├── agent_plans/          (设计方案 .md)
   ├── agent_configs/        (配置文件 .yaml)
   └── deployed_*            (已部署配置)

📝 监控日志:
   /tmp/i_queue_logs_*.txt   (手动导出)
```

---

## 获取帮助

```bash
# 查看 API 文档
http://localhost:8000/docs

# 阅读用户指南
cat AGENT_AUTODESIGNER_GUIDE.md

# 查看设计示例
cat mnt/user-data/outputs/agent_plans/plan_1.md
```

---

## 下一步

✨ **现在就尝试吧！**

```bash
# 1. 启动完整模式
python run.py

# 2. 选择: 1️⃣ 完整模式

# 3. 在设计器中输入需求:
#    "帮我总结今天的工作内容"

# 4. 点击 "智能分析"

# 5. 查看监控面板的实时日志

# 6. 享受自动化的 Agent 设计体验！
```

---

**🎉 祝你使用愉快！**

更多信息: [README.md](README.md) | [AGENT_AUTODESIGNER_GUIDE.md](AGENT_AUTODESIGNER_GUIDE.md)
