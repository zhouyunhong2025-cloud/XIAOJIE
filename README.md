# 🔧 AgentForge

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square&logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Alpha-orange?style=flat-square)]()

**用 Python 函数替代一大堆文字 Prompt 来定义 AI 智能体**

[快速开始](#快速开始) • [文档](#文档) • [示例](#示例) • [问题反馈](../../issues)

</div>

---

## 📌 核心问题

传统 AI 智能体需要维护一堆文本文件：

```
system_prompt.txt      ← 500 行描述
skills.md              ← 200 行能力说明
rules.txt              ← 100 行规则
alignment_guide.md     ← 300 行对齐指南
```

**这很痛苦** 😫

---

## ✨ 解决方案：AgentForge

**把一切变成可执行的 Python 代码**

```python
# 技能 = 装饰器函数
@skill(name="understand_intent")
def understand(text: str) -> dict: ...

# 规则 = 约束函数  
@rule(name="no_harmful")
def no_harmful(text: str) -> tuple: ...

# 管道 = 执行顺序
pipeline = Pipeline([
    Phase("understand", understand),
    Phase("reason", reason_fn),
    Phase("format", format_fn),
])

# 对齐 = 加权公式
alignment = AlignmentFormula([
    AlignmentDimension("safety", weight=0.4),
    AlignmentDimension("helpfulness", weight=0.35),
])

# 组装智能体
agent = Agent(pipeline=pipeline, alignment=alignment)
```

---

## 🎯 核心特性

| 特性 | 传统方式 | AgentForge |
|-----|---------|-----------|
| **技能定义** | 文字描述 | Python 函数 |
| **规则管理** | 文本文件 | 代码约束 |
| **执行流程** | 隐含在 Prompt | 显式 Pipeline |
| **对齐验证** | 主观指南 | 量化公式 |
| **调试能力** | 困难 | 每阶段可追踪 |

---

## 🚀 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/zhouyunhong2025-cloud/XIAOJIE.git
cd XIAOJIE/I.QUEUE
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 运行示例

```bash
python example_agent.py
```

**预期输出：**

```
╔══════════════════════════════════════╗
  Agent: DemoAgent
  📦 Skills (3):
     • understand_intent [priority=10]
     • chain_of_thought  [priority=8]
     • format_output     [priority=5]
  ⚖️  Alignment Score: 0.965 (PASS ✅)
╚══════════════════════════════════════╝
```

---

## 📁 项目结构

```
XIAOJIE/
├── I.QUEUE/                    ← 主项目目录
│   ├── agentforge/
│   │   ├── core/
│   │   │   ├── agent.py       # Agent 主类
│   │   │   ├── skill.py       # @skill 装饰器
│   │   │   ├── rule.py        # @rule 约束引擎
│   │   │   ├── pipeline.py    # Pipeline 执行管道
│   │   │   └── alignment.py   # 对齐公式计算
│   │   └── __init__.py
│   ├── demo/
│   │   └── example_agent.py   # 完整使用示例
│   ├── pyproject.toml         # 项目配置
│   ├── requirements.txt       # 依赖
│   └── README.md              # 详细文档 →
└── README.md                  # 本文件
```

---

## 📖 核心 API

### @skill — 定义技能

```python
@skill(name="translate", tags=["language"], priority=7)
def translate_text(text: str, target_lang: str = "en") -> str:
    """将文本翻译为目标语言。"""
    return f"Translated: {text} to {target_lang}"
```

### @rule — 定义规则

```python
@rule(name="max_length", severity="warn")
def check_length(output: str) -> tuple[bool, str]:
    ok = len(output) < 1000
    return ok, "输出超过 1000 个字符"
```

### Pipeline — 定义执行顺序

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
