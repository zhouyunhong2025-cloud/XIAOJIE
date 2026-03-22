#!/usr/bin/env python3
"""
🤖 I.QUEUE Agent 自动设计系统 - 快速启动脚本

使用方法:
    python quick_start.py "你的需求描述"
    python quick_start.py "帮我总结今天的工作"
    python quick_start.py "为我精选最新新闻"
"""

import sys
import os
from pathlib import Path

# 添加 I.QUEUE 目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent_auto_designer import AgentAutoDesigner


def main():
    """主函数"""
    
    # 欢迎信息
    print("\n" + "="*70)
    print("🤖 I.QUEUE Agent 自动设计系统")
    print("="*70)
    print("\n✨ 一句话描述你的需求，我们为你自动设计最优 Agent 配置！\n")
    
    # 获取用户需求
    if len(sys.argv) > 1:
        # 从命令行参数获取
        requirement = " ".join(sys.argv[1:])
        print(f"📌 你的需求: {requirement}\n")
    else:
        # 交互式输入
        print("请描述你的需求 (例如: 帮我总结今天的工作):")
        requirement = input(">>> ").strip()
        
        if not requirement:
            print("❌ 需求不能为空！")
            sys.exit(1)
    
    print("\n" + "-"*70 + "\n")
    
    # 创建设计师
    designer = AgentAutoDesigner()
    
    # 开始设计
    try:
        plan = designer.design_agent(requirement)
    except Exception as e:
        print(f"❌ 设计过程出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # 显示完整方案
    print("\n" + "="*70)
    print("\n📋 完整设计方案\n")
    print(plan.to_markdown())
    
    # 导出选项
    print("\n" + "="*70)
    print("\n📤 导出选项:\n")
    
    # 生成文件名
    import time
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"agent_{timestamp}"
    
    # 导出 Markdown
    md_path = designer.export_plan_markdown(plan, filename)
    print(f"✅ Markdown 文档已导出")
    print(f"   可读路径: {md_path}")
    
    # 导出 YAML
    yaml_path = designer.export_plan_yaml(plan, filename)
    print(f"✅ YAML 配置已导出")
    print(f"   执行路径: {yaml_path}")
    
    # 下一步建议
    print("\n" + "="*70)
    print("\n🚀 下一步:\n")
    print("1. 📖 查看 Markdown 文档，确认所有配置无误")
    print(f"   打开: {md_path}")
    print()
    print("2. ✏️  如需修改，编辑 Markdown 或 YAML 文件")
    print()
    print("3. 🎯 确认无误后，复制 Agent 配置启动你的 Agent")
    print(f"   配置: {yaml_path}")
    print()
    print("4. 💬 有问题? 查看详细指南: AGENT_AUTODESIGNER_GUIDE.md")
    
    print("\n" + "="*70)
    print("\n✨ Agent 设计完成！祝你使用愉快~ 🎉\n")


if __name__ == "__main__":
    main()
