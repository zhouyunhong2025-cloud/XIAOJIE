"""
AgentForge v1 — Quickstart
===========================

Run this file to see all three resolution levels.
Set your API key first:
    export OPENAI_API_KEY=sk-...
    # or
    export ANTHROPIC_API_KEY=sk-ant-...

Then:
    python demo/quickstart.py
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from agentforge.cartridges import AssistantCartridge


def demo_beginner():
    print("\n" + "="*55)
    print("  分辨率: BEGINNER  (新手模式 — 3行代码)")
    print("="*55)
    print("""
    from agentforge.cartridges import AssistantCartridge
    agent = AssistantCartridge(llm="openai").build()
    result = agent.run("帮我写一个会议通知")
    """)

    # Offline simulation (no real API key needed for demo)
    cartridge = AssistantCartridge(
        llm=_mock_llm("收到！会议通知如下：\n\n各位同事，\n定于明日上午10:00召开项目周会，请准时参加。"),
        resolution="beginner",
        memory_path=None,
        verbose=True,
    )
    agent = cartridge.build()
    result = agent.run("帮我写一个会议通知")
    print(f"\n回复:\n{result['output']}")


def demo_standard():
    print("\n" + "="*55)
    print("  分辨率: STANDARD  (有一定基础)")
    print("="*55)

    cartridge = AssistantCartridge(
        llm=_mock_llm("根据我的分析：这个问题涉及三个方面...\n1. 首先...\n2. 其次...\n3. 最后..."),
        resolution="standard",        # ← 开启 chain-of-thought
        persona="你是一位专业的技术顾问，回答要有条理。",
        memory_path=None,
        verbose=True,
    )
    agent = cartridge.build()

    # 记忆跨轮持久
    cartridge.remember("user_role", "产品经理", layer="session")
    cartridge.remember("project",   "AgentForge开源项目", layer="session")

    result = agent.run("我们项目的核心用户是谁？")
    print(f"\n回复:\n{result['output']}")
    print(f"\n内存状态:\n{cartridge.memory.summarize()}")


def demo_expert():
    print("\n" + "="*55)
    print("  分辨率: EXPERT  (自定义所有模块)")
    print("="*55)
    print("  高级用户可以替换任意模块，容器结构不变")
    print("""
    # 自定义规则
    @rule(name="must_cite", severity="warn")
    def must_include_citation(output: str):
        return "参考" in output or "来源" in output, "Missing citation"

    # 自定义对齐维度
    alignment = AlignmentFormula([
        AlignmentDimension("domain_accuracy", weight=0.6, scorer=my_scorer),
        AlignmentDimension("safety",          weight=0.4, scorer=...),
    ])

    # 用 expert 分辨率传入
    cartridge = AssistantCartridge(resolution="expert", ...)
    """)
    print("  → 方块更小，精度更高，容器规则完全不变")


# ── Mock LLM for offline demo ─────────────────────────────────────────────────

def _mock_llm(fixed_response: str):
    """Returns a fake LLM backend that always returns the same string."""
    from agentforge.llm.base import LLMBackend, LLMResponse, Message
    from typing import List, Optional

    class MockLLM(LLMBackend):
        def complete(self, messages: List[Message], system: Optional[str] = None) -> LLMResponse:
            return LLMResponse(text=fixed_response, model="mock", input_tokens=10, output_tokens=20)

    return MockLLM()


if __name__ == "__main__":
    demo_beginner()
    demo_standard()
    demo_expert()

    print("\n" + "="*55)
    print("  接入真实 LLM 只需改一行:")
    print("="*55)
    print("""
  # OpenAI
  agent = AssistantCartridge(llm="openai").build()

  # Anthropic Claude
  agent = AssistantCartridge(llm="anthropic").build()

  # 指定模型
  agent = AssistantCartridge(llm="openai", model="gpt-4o").build()
    """)
