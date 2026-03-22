#!/usr/bin/env python3
"""
🤖 I.QUEUE Complete Launcher
Starts Web Server + Desktop Monitoring Panel together
"""

import sys
import subprocess
import time
import os
from pathlib import Path


def main():
    """Main launch function"""
    
    print("\n" + "="*70)
    print("🤖 I.QUEUE Agent Design & Execution System")
    print("="*70)
    print("\nSelect startup mode:\n")
    
    print("1️⃣  Full Mode (Web + Desktop Monitor)")
    print("   → Design Agent in browser")
    print("   → Monitor execution in desktop panel")
    print()
    
    print("2️⃣  Web Only Mode (Browser)")
    print("   → Access http://localhost:8000")
    print()
    
    print("3️⃣  CLI Only Mode (Command Line)")
    print("   → python quick_start.py 'your requirement'")
    print()
    
    choice = input("Choose (1/2/3): ").strip()
    
    if choice == "1":
        start_full_mode()
    elif choice == "2":
        start_web_only()
    elif choice == "3":
        print("\n✅ Using CLI Mode:")
        print("   cd /path/to/I.QUEUE")
        print("   python quick_start.py 'your requirement'\n")
    else:
        print("❌ Invalid choice")
        sys.exit(1)


def start_full_mode():
    """Full mode: Web + Monitor Panel"""
    
    print("\n" + "="*70)
    print("Startup: Full Mode (Web + Desktop Monitor)")
    print("="*70 + "\n")
    
    # Get project path
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    # Check dependencies
    print("📦 Checking dependencies...")
    try:
        import fastapi
        import uvicorn
        print("  ✓ FastAPI/Uvicorn")
    except ImportError:
        print("  ⚠️  Missing FastAPI")
        print("  Run: pip install fastapi uvicorn")
        sys.exit(1)
    
    try:
        from PyQt6.QtWidgets import QApplication
        print("  ✓ PyQt6")
    except ImportError:
        print("  ⚠️  Missing PyQt6")
        print("  Run: pip install PyQt6")
        sys.exit(1)
    
    print("\n")
    
    # Start Web Server (background)
    print("🌐 Starting Web Server...")
    web_process = subprocess.Popen(
        [sys.executable, "web_server.py"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    print("   ✓ Web server starting...")
    
    # Wait for Web Server to be ready
    time.sleep(2)
    
    print("   ✓ Web server running at http://localhost:8000")
    print()
    
    # Start Desktop Monitor
    print("🖥️  Starting Desktop Monitor Panel...")
    try:
        subprocess.run([sys.executable, "agent_monitor.py"])
    except KeyboardInterrupt:
        print("\n\nShutting down...")
        web_process.terminate()
        web_process.wait(timeout=5)
    except Exception as e:
        print(f"❌ Failed to start monitor panel: {e}")
        web_process.terminate()
        sys.exit(1)
    
    # Cleanup
    print("\n✅ I.QUEUE Closed")


def start_web_only():
    """Web only mode"""
    
    print("\n" + "="*70)
    print("Startup: Web Mode")
    print("="*70)
    print("\n🌐 Web Server starting...")
    print("   🔗 Access: http://localhost:8000")
    print("   📖 Docs: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop server\n")
    
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    try:
        subprocess.run([sys.executable, "web_server.py"])
    except KeyboardInterrupt:
        print("\n✅ Web server closed")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
