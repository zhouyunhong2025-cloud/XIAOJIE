# 🔧 AgentForge

**用 Python 函数替代一大堆文字 Prompt 来定义 AI 智能体**

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square&logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Demo-orange?style=flat-square)]()

---

## 💡 核心理念

传统方式需要维护一堆文本文件：

```
system_prompt.txt      ← 500 行文字描述
skills_description.md  ← 200 行能力说明
rules.txt              ← 100 行规则列表
alignment_guide.md     ← 300 行对齐指南
```

**AgentForge** 把这一切变成可执行的 Python 代码：

```python
# 技能 = 装饰器函数
@skill(name="understand_intent", priority=10)
def understand_intent(text: str) -> dict: ...

# 规则 = 约束函数
@rule(name="no_harmful", severity="block")
def no_harmful_input(text: str) -> tuple: ...

# 分阶段执行 = Pipeline
pipeline = Pipeline([
    Phase("understand_intent", intent_phase),
    Phase("chain_of_thought",  reasoning_phase),
    Phase("format_output",     output_phase),
])

# 对齐 = 加权公式
#   score = 0.40×harmlessness + 0.35×helpfulness + 0.25×conciseness
alignment = AlignmentFormula([
    AlignmentDimension("harmlessness", weight=0.40, scorer=..., floor=0.75),
    AlignmentDimension("helpfulness",  weight=0.35, scorer=..., floor=0.50),
    AlignmentDimension("conciseness",  weight=0.25, scorer=...),
])

# 组装智能体
agent = Agent(name="MyAgent", pipeline=pipeline, alignment=alignment)
result = agent.run("Calculate 42 * 7")
```

---

## ✨ 特性

| 模块 | 传统方式 | AgentForge |
|------|---------|------------|
| **技能定义** | 文字描述列表 | `@skill` 装饰器函数 |
| **行为规则** | 规则文本文件 | `@rule` 约束函数 |
| **执行顺序** | 隐含在 Prompt 里 | 显式 `Pipeline` 阶段 |
| **对齐验证** | 主观文字指南 | 可计算的加权公式 |
| **调试** | 几乎不可能 | 每个阶段有计时和状态 |

---

## 🚀 快速开始

```bash
git clone https://github.com/YOUR_USERNAME/agentforge.git
cd agentforge
python demo/example_agent.py
```

运行输出示例：

```
╔══════════════════════════════════════╗
  Agent: DemoAgent
  📦 Skills (3):
     • understand_intent [priority=10]
     • chain_of_thought  [priority=8]
     • format_output     [priority=5]
  📏 Rules (2):
     • no_harmful_input [block]
     • output_not_empty [error]
  🔗 Pipeline:
     understand_intent → chain_of_thought → format_output
  ⚖️  Alignment:
     score = 0.40×harmlessness + 0.35×helpfulness + 0.25×conciseness
╚══════════════════════════════════════╝

Alignment Score: 0.965 (PASS ✅)
  harmlessness   [████████████████████] 1.000
  helpfulness    [██████████████████░░] 0.900
  conciseness    [████████████████████] 1.000
```

---

## 📁 项目结构

```
agentforge/
├── agentforge/
│   ├── core/
│   │   ├── skill.py       # @skill 装饰器系统
│   │   ├── rule.py        # @rule 约束引擎
│   │   ├── pipeline.py    # 分阶段执行管道
│   │   ├── alignment.py   # 对齐公式计算
│   │   └── agent.py       # Agent 主类
│   └── __init__.py
├── demo/
│   └── example_agent.py   # 完整示例
└── README.md
```

---

## 📖 核心 API

### `@skill` — 定义技能

```python
@skill(name="translate", tags=["language"], priority=7)
def translate(text: str, target_lang: str = "en") -> str:
    """Translate text to target language."""
    ...
```

### `@rule` — 定义规则

```python
@rule(name="max_length", severity="warn", phase="post")
def check_length(output: str) -> tuple[bool, str]:
    ok = len(output) < 1000
    return ok, "Output exceeds 1000 characters"
```

### `Pipeline` — 定义执行顺序

```python
pipeline = Pipeline([
    Phase("step1", fn1),
    Phase("step2", fn2, condition=lambda ctx: ctx.get("step1") is not None),
    Phase("step3", fn3),
])
```

### `AlignmentFormula` — 量化对齐

```python
formula = AlignmentFormula(
    dimensions=[
        AlignmentDimension("safety",  weight=0.5, scorer=safety_scorer,  floor=0.8),
        AlignmentDimension("quality", weight=0.5, scorer=quality_scorer, floor=0.6),
    ],
    threshold=0.70,
)
report = formula.evaluate(agent_output)
print(report)  # 可视化评分条
```

---

## 🗺️ 路线图

- [ ] 支持 LLM 后端接入（OpenAI / Anthropic）
- [ ] 技能依赖图自动解析
- [ ] 对齐分数历史追踪
- [ ] YAML/JSON 配置导出
- [ ] Web UI 可视化 Pipeline

---

## 📄 License

MIT © 2025
