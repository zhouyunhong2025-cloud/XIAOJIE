# I.QUEUE

<div align="center">

![I.QUEUE Tetris Demo](https://img.shields.io/badge/Demo-Live%20Preview-3498db?style=for-the-badge&logo=javascript)  
[![Python](https://img.shields.io/badge/Python-3.9+-2ecc71?style=flat-square&logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-3498db?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Alpha-e74c3c?style=flat-square)]()

**Intelligence. Order. A gift for you and your AI agent.**

[🎮 Live Demo](#demo) — [📖 Documentation](#documentation) — [🚀 Quick Start](#quick-start) — [💬 Issues](../../issues)

</div>

---

## 🎨 Product Showcase

**AI agents made simple. Stack capabilities like Tetris blocks.**

![I.QUEUE Tetris Game Demo](./docs/tetris-demo.png)

### Brand Identity

![I.QUEUE Logo](./docs/i-queue-logo.png)

### Three Core Building Blocks (Stacked Together)

| Block Type | Visual | Meaning | Description |
|-----------|--------|---------|-------------|
| **Memory Rod** | `║` | "I remember our agreement" | Persistent knowledge layer spanning all stages |
| **Skill Block** | `■` | "My new skill learned" | Capabilities defined as Python functions |
| **Alignment** | `▲` | "I love what you love" | Quantified values with weighted formulas |

Watch them combine to form your agent pipeline in three stages:

| Stage | Key Concepts | Result |
|-------|-------------|--------|
| **Input Processing** | Skills + Memory | Context Preparation |
| **Reasoning** | Mix with Alignment | Decision Making |
| **Output** | Final Composition | Agent Response |

**All working together in perfect order.** ✓

**[→ View Full Interactive Showcase](https://zhouyunhong2025-cloud.github.io/XIAOJIE/showcase.html)**

---

## What is I.QUEUE?

**Build AI agents with Python functions—not giant text prompts.**

Traditional AI agent development means maintaining mountains of configuration:

```
system_prompt.txt      (500 lines)
skills_description.md  (200 lines)
rules.txt              (100 lines)
alignment_guide.md     (300 lines)
… it never ends
```

**I.QUEUE** transforms this chaos into clean, executable Python code.

---

## The Concept

Think of building an agent like stacking Tetris blocks—each piece represents a capability (skill, rule, memory, alignment). Drop blocks in, watch them settle, and your agent takes shape.

**That's it.** Simple. Organized. Powerful.

### Try the live demo: [I.QUEUE Interactive Playground](https://zhouyunhong2025-cloud.github.io/XIAOJIE/)

---

## How It Works

Instead of paragraphs of text, define everything as code:

```python
# A skill = a typed Python function with metadata
@skill(name="understand_intent", priority=10)
def understand_intent(text: str) -> dict:
    """Extract user intent from input."""
    return {"intent": "...", "confidence": 0.95}

# A rule = an executable constraint
@rule(name="no_harmful_output", severity="block")
def check_safety(output: str) -> tuple[bool, str]:
    is_safe = not contains_harm(output)
    return is_safe, "Output violates safety policy"

# Pipeline = explicit execution order
pipeline = Pipeline([
    Phase("input_analysis", understand_intent),
    Phase("reasoning", chain_of_thought),
    Phase("output_formatting", format_response),
])

# Alignment = quantifiable scoring formula
alignment = AlignmentFormula([
    AlignmentDimension("safety", weight=0.40, scorer=safety_scorer),
    AlignmentDimension("helpfulness", weight=0.35, scorer=help_scorer),
    AlignmentDimension("conciseness", weight=0.25, scorer=brief_scorer),
])

# Assemble the agent
agent = Agent(
    name="MyAgent",
    pipeline=pipeline,
    alignment=alignment,
    llm_backend="openai"
)

# Run it
result = agent.run("What is machine learning?")
print(result.output)
print(f"Alignment score: {result.alignment_score}")
```

---

## Core Building Blocks

| Block | Represents | Purpose |
|-------|-----------|---------|
| **Skill** | Function + metadata | Define capabilities as code |
| **Rule** | Constraint logic | Executable guardrails |
| **Pipeline** | Explicit stages | Structure execution flow |
| **Alignment** | Weighted formula | Quantified value scoring |
| **Memory** | Layered storage | Flash → session → persistent |
| **Cartridge** | Pre-built preset | Quick start configurations |

---

## Key Advantages

| Aspect | Traditional | I.QUEUE |
|--------|-----------|---------|
| Skill Definition | Text descriptions | Python functions |
| Rule Management | Config files | Code constraints |
| Execution Flow | Hidden in prompts | Explicit pipeline |
| Alignment | Vague guidelines | Computed formula |
| Debugging | Nearly impossible | Stage-by-stage tracking |
| Version Control | Hard to diff | Full git support |
| Testing | Manual | Automated |

---

## Quick Start

### Download the Project

**Option 1: Clone via Git** (recommended)
```bash
git clone https://github.com/zhouyunhong2025-cloud/XIAOJIE.git
cd XIAOJIE/I.QUEUE
```

**Option 2: Download ZIP**
- Go to [GitHub Releases](../../releases) and download the latest version
- Extract the ZIP file and navigate to the `I.QUEUE` folder

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Example

```bash
python example_agent.py
```

### Try the Interactive Demo

[🎮 **Live Tetris Demo** - See Agent Assembly in Action](https://zhouyunhong2025-cloud.github.io/XIAOJIE/)

---

## Three Ways to Use I.QUEUE

**Beginner** — Zero config, sensible defaults
```python
from iqueue.cartridges import AssistantCartridge
agent = AssistantCartridge(llm="openai").build()
result = agent.run("Write a summary of quantum computing")
```

**Standard** — Customizable components
```python
agent = Agent(
    skills=[understand_skill, reason_skill],
    rules=[safety_rule, output_rule],
    pipeline=my_pipeline,
    llm_backend="openai"
)
```

**Expert** — Full control
```python
# Write your own @skill, @rule, Pipeline, AlignmentFormula
# Combine them however you want
# Unlimited customization power
```

---

## More Info

- **Full Documentation**: [I.QUEUE Framework Guide](./I.QUEUE/README.md)
- **Live Interactive Demo**: [Tetris Playground](https://zhouyunhong2025-cloud.github.io/XIAOJIE/)
- **Visual Showcase**: [Premium Product Demo](https://zhouyunhong2025-cloud.github.io/XIAOJIE/showcase.html)

---

## Documentation

Full API reference and tutorials in [I.QUEUE/README.md](I.QUEUE/README.md)

- [Core Concepts](I.QUEUE/README.md#core-concepts)
- [API Reference](I.QUEUE/README.md#api-reference)
- [Examples](I.QUEUE/example_agent.py)
- [Advanced Usage](I.QUEUE/README.md#advanced-patterns)

---

## Project Structure

```
XIAOJIE/
├── I.QUEUE/                        # Main package
│   ├── core/
│   │   ├── agent.py               # Agent orchestrator
│   │   ├── skill.py               # @skill decorator
│   │   ├── rule.py                # @rule decorator
│   │   ├── pipeline.py            # Pipeline execution
│   │   ├── alignment.py           # Alignment scoring
│   │   └── memory.py              # Memory system
│   ├── llm/                        # LLM backends
│   │   ├── openai_backend.py
│   │   └── anthropic_backend.py
│   ├── example_agent.py           # Usage demo
│   ├── pyproject.toml             # Package config
│   └── requirements.txt           # Dependencies
├── docs/                          # GitHub Pages
│   └── index.html                 # Live Tetris demo
└── README.md                      # This file
```

---

## What's Next

- [ ] Interactive tutorials
- [ ] More pre-built cartridges
- [ ] PyPI package release
- [ ] GitHub Actions CI/CD
- [ ] Agent templates library
- [ ] Performance optimization

---

## License

MIT License — see [LICENSE](LICENSE)

---

<div align="center">

**Made with care for developers and AI agents.**  
[GitHub](https://github.com/zhouyunhong2025-cloud/XIAOJIE) — [Issues](../../issues) — [Discussions](../../discussions)

</div>
  Agent: DemoAgent
  📦 Skills (3):
     • understand_intent [priority=10]
     • chain_of_thought  [priority=8]
     • format_output     [priority=5]
  ⚖️  Alignment Score: 0.965 (PASS ✅)
╚══════════════════════════════════════╝
```

---

## Project Structure

```
XIAOJIE/
├── I.QUEUE/                        # Main package directory
│   ├── core/
│   │   ├── agent.py               # Agent orchestrator class
│   │   ├── skill.py               # @skill decorator system
│   │   ├── rule.py                # @rule constraint engine
│   │   ├── pipeline.py            # Pipeline execution flow
│   │   └── alignment.py           # Alignment formula calculation
│   ├── llm/
│   │   ├── openai_backend.py      # OpenAI integration
│   │   └── anthropic_backend.py   # Anthropic integration
│   ├── memory.py                  # Memory system
│   ├── example_agent.py           # Complete usage example
│   ├── pyproject.toml             # Project configuration
│   ├── requirements.txt           # Dependencies
│   └── README.md                  # Detailed API docs
├── docs/                          # GitHub Pages deployment
│   ├── index.html                 # Interactive Tetris demo
│   └── showcase.html              # Product showcase page
└── README.md                      # This file
```

---

## Core API

### `@skill` — Define a Skill

```python
@skill(name="translate", tags=["language"], priority=7)
def translate_text(text: str, target_lang: str = "en") -> str:
    """Translate text to target language."""
    return f"Translated: {text} to {target_lang}"
```

### `@rule` — Define a Rule

```python
@rule(name="max_length", severity="warn")
def check_length(output: str) -> tuple[bool, str]:
    ok = len(output) < 1000
    return ok, "Output exceeds 1000 characters"
```

### `Pipeline` — Define Execution Order

```python
pipeline = Pipeline([
    Phase("analyze", analyze_fn),
    Phase("process", process_fn),
    Phase("output", format_fn),
])
```

### AlignmentFormula — 量化对齐

```python
alignment = AlignmentFormula([
    AlignmentDimension("safety", weight=0.40, scorer=safety_scorer),
    AlignmentDimension("helpfulness", weight=0.35, scorer=helpfulness_scorer),
    AlignmentDimension("conciseness", weight=0.25, scorer=conciseness_scorer),
])
```

---

## 📚 详细文档

更多内容和高级用法请查看 **[I.QUEUE/README.md](I.QUEUE/README.md)**

- [API 详细说明](I.QUEUE/README.md#-核心-api)
- [完整示例](I.QUEUE/example_agent.py)
- [配置选项](I.QUEUE/pyproject.toml)

---

## 🔗 相关资源

- 🐍 **Python 3.9+** 支持
- 📦 支持 **OpenAI** 和 **Anthropic** LLM 后端
- 🧠 内置 **记忆系统** 和 **对齐验证**
- 🔧 易于自定义和扩展

---

## 📝 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

<div align="center">

**Made with ❤️ by AgentForge Contributors**

</div>
