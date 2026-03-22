#!/usr/bin/env python3
"""
🤖 I.QUEUE Agent Auto-Design System - Quick Start Script

Usage:
    python quick_start.py "Your requirement description"
    python quick_start.py "Summarize my daily work"
    python quick_start.py "Curate the latest news for me"
"""

import sys
import os
from pathlib import Path

# Add I.QUEUE directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent_auto_designer import AgentAutoDesigner


def main():
    """Main function"""
    
    # Welcome message
    print("\n" + "="*70)
    print("🤖 I.QUEUE Agent Auto-Design System")
    print("="*70)
    print("\n✨ Describe your need in one sentence - we'll auto-design the perfect Agent!\n")
    
    # Get user requirement
    if len(sys.argv) > 1:
        # From command line arguments
        requirement = " ".join(sys.argv[1:])
        print(f"📌 Your Requirement: {requirement}\n")
    else:
        # Interactive input
        print("Describe what you need (e.g., Summarize my daily work):")
        requirement = input(">>> ").strip()
        
        if not requirement:
            print("❌ Requirement cannot be empty!")
            sys.exit(1)
    
    print("\n" + "-"*70 + "\n")
    
    # Create designer
    designer = AgentAutoDesigner()
    
    # Start design
    try:
        plan = designer.design_agent(requirement)
    except Exception as e:
        print(f"❌ Error during design process: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Display complete plan
    print("\n" + "="*70)
    print("\n📋 Complete Design Plan\n")
    print(plan.to_markdown())
    
    # Export options
    print("\n" + "="*70)
    print("\n📤 Export Options:\n")
    
    # Generate filename
    import time
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"agent_{timestamp}"
    
    # Export Markdown
    md_path = designer.export_plan_markdown(plan, filename)
    print(f"✅ Markdown document exported")
    print(f"   Path: {md_path}")
    
    # Export YAML
    yaml_path = designer.export_plan_yaml(plan, filename)
    print(f"✅ YAML configuration exported")
    print(f"   Path: {yaml_path}")
    
    # Next steps
    print("\n" + "="*70)
    print("\n🚀 Next Steps:\n")
    print("1. 📖 Review the Markdown document to verify all settings")
    print(f"   Open: {md_path}")
    print()
    print("2. ✏️  Edit Markdown or YAML file if you need to customize")
    print()
    print("3. 🎯 Once verified, use the Agent configuration to start")
    print(f"   Config: {yaml_path}")
    print()
    print("4. 💬 Have questions? See the guide: AGENT_AUTODESIGNER_GUIDE.md")
    
    print("\n" + "="*70)
    print("\n✨ Agent design complete! Enjoy! 🎉\n")


if __name__ == "__main__":
    main()
