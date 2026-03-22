# Startup Guide

## Three Ways to Start

### Method 1️⃣: Complete Mode (Recommended)

**Web UI + Desktop Monitor + One-Click Deploy**

```bash
cd I.QUEUE
python run.py
# Select: 1️⃣ Complete Mode
```

**What you'll see:**
1. 🌐 Web browser opens designer (http://localhost:8000)
2. 🖥️ Desktop floating monitor panel
   - 📋 Real-time logs
   - 📊 Execution stats
   - ⚙️ Quick actions

**Workflow:**
```
Enter requirement
  ↓
Click "Smart Analyze"
  ↓
Review design report
  ↓
Click "Deploy"
  ↓
Monitor panel shows live logs ✨
```

---

### Method 2️⃣: Web Only

**Browser-based, no desktop apps needed**

```bash
cd I.QUEUE
python web_server.py
```

**Access:**
- 🌐 Web UI: http://localhost:8000
- 📚 API Docs: http://localhost:8000/docs

---

### Method 3️⃣: CLI Only

**Command-line quick testing**

```bash
cd I.QUEUE
python quick_start.py "your requirement"
```

**Example:**
```bash
python quick_start.py "summarize today's work"
# Auto-generates: agent_plan_YYYYMMDD_HHMMSS.md + configs
```

---

## Install Dependencies

```bash
# Standard (all features)
pip install -r requirements.txt

# Minimal (Web only)
pip install fastapi uvicorn requests

# Full (with desktop app)
pip install -r requirements.txt
pip install PyQt6
```

---

## Desktop Monitor Panel

### Features

| Tab | Function | Purpose |
|-----|----------|---------|
| 📋 Real-time Logs | System logs | Track execution |
| 📊 Stats | Performance metrics | View statistics |
| ⚙️ Quick Actions | Control buttons | Manage system |

### Quick Action Buttons

```
🌐 Open Web UI
   → Open designer

📂 Open Output Folder
   → View generated files

🔄 Refresh Status
   → Update system status

📋 Export Logs
   → Save execution logs

⚠️ Clear Logs
   → Clear log files
```

### Monitor Window Layout

```
Floating on right side
(500px wide × 700px tall)

Always on top
━━━━━━━━━━━━━━━━━━━━
│  🤖 I.QUEUE Monitor │
│                    │
│  Status: ✅ Online │
│  [Progress bar]    │
│                    │
│  📋 Real-time Logs │
│  System output     │
│  ...               │
│                    │
│  [Button group]    │
━━━━━━━━━━━━━━━━━━━━
```

---

## Troubleshooting

### Q: Can't connect to http://localhost:8000

**Solution:**
```bash
# Check if port is in use
lsof -i :8000

# If occupied, use different port
python -m uvicorn web_server:app --port 8001
```

### Q: PyQt6 installation fails

**Solution:**
```bash
# Ubuntu/Debian
sudo apt-get install python3-pyqt6

# macOS
brew install python-pyqt6

# Or use pip
pip install PyQt6 --upgrade
```

### Q: API connection errors

**Solution:**
1. Ensure web server is running
2. Check firewall settings
3. Review logs for debugging

### Q: Monitor panel shows no logs

**Solution:**
1. Check if API is working
2. Click "Refresh Status" in panel
3. Restart application

---

## Advanced Usage

### Custom Port

```bash
# Start on port 9000
python -m uvicorn web_server:app --host 0.0.0.0 --port 9000
```

### Remote Access

```bash
# Allow other computers to connect
python -m uvicorn web_server:app --host 0.0.0.0 --port 8000
# Access from other machine: http://your-ip:8000
```

### Run in Background

```bash
# Linux/macOS
nohup python web_server.py > server.log 2>&1 &

# Using screen
screen -S i_queue
python web_server.py
# Press Ctrl+A, D to exit

# Using tmux
tmux new-session -d -s i_queue
tmux send-keys -t i_queue "python web_server.py" Enter
```

---

## Keyboard Shortcuts

### Web UI

| Shortcut | Function |
|----------|----------|
| Ctrl+Enter | Submit requirement |
| Drag-drop | Select components |

### Monitor Panel

| Shortcut | Function |
|----------|----------|
| Ctrl+C | Close application |
| Click | Quick actions |

---

## Performance Tips

### System Requirements
- **Minimum**: Python 3.10+, 4GB RAM, 50MB disk
- **Recommended**: Python 3.10+, 8GB RAM, 100MB disk

### Optimization Tips
1. **Close unused tabs** to reduce memory
2. **Export logs regularly** to clear runtime logs
3. **Clean output folder** (~mnt/user-data/outputs)
4. **Update dependencies** `pip install -r requirements.txt --upgrade`

---

## Log Locations

```
📂 Generated files:
   /workspaces/XIAOJIE/I.QUEUE/mnt/user-data/outputs/
   ├── agent_plans/          (Design plans .md)
   ├── agent_configs/        (Config files .yaml)
   └── deployed_*            (Deployed configs)

📝 Monitor logs:
   /tmp/i_queue_logs_*.txt   (Manual export)
```

---

## Get Help

```bash
# View API documentation
http://localhost:8000/docs

# Read user guide
cat AGENT_AUTODESIGNER_GUIDE.md

# Check design examples
cat mnt/user-data/outputs/agent_plans/plan_1.md
```

---

## Next Steps

✨ **Try it now!**

```bash
# 1. Start complete mode
python run.py

# 2. Select: 1️⃣ Complete Mode

# 3. In designer, enter requirement:
#    "Summarize today's work"

# 4. Click "Smart Analyze"

# 5. Watch monitor panel's live logs

# 6. Enjoy automated agent design!
```

---

**🎉 Happy using!**

更多信息: [README.md](README.md) | [AGENT_AUTODESIGNER_GUIDE.md](AGENT_AUTODESIGNER_GUIDE.md)
