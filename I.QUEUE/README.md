# I.QUEUE

**Build AI agents with Python functions—not giant text prompts.**

[![Python](https://img.shields.io/badge/Python-3.9+-2ecc71?style=flat-square&logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-3498db?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Alpha-e74c3c?style=flat-square)]()

---

## Core Philosophy

Traditional AI agent development requires maintaining piles of configuration files:

```
system_prompt.txt      (500 lines)
skills_description.md  (200 lines)
rules.txt              (100 lines)
alignment_guide.md     (300 lines)
… more config files
```

**I.QUEUE** transforms all of this into clean, executable Python code.

---

## The Idea

Define everything as code:

```python
# A skill = a typed Python function with metadata
@skill(name="understand_intent", priority=10)
def understand_intent(text: str) -> dict:
    """Extract user intent from input."""
    return {"intent": "...", "confidence": 0.95}

# A rule = an executable constraint
@rule(name="no_harmful", severity="block")
def check_safety(output: str) -> tuple[bool, str]:
    is_safe = not contains_harm(output)
    return is_safe, "Output violates safety policy"

# Pipeline = explicit execution order
pipeline = Pipeline([
    Phase("input_analysis", understand_intent),
    Phase("reasoning", chain_of_thought),
    Phase("output_formatting", format_response),
])

# Alignment = quantifiable formula
#   score = 0.40×harmlessness + 0.35×helpfulness + 0.25×conciseness
alignment = AlignmentFormula([
    AlignmentDimension("harmlessness", weight=0.40, scorer=..., floor=0.75),
    AlignmentDimension("helpfulness",  weight=0.35, scorer=..., floor=0.50),
    AlignmentDimension("conciseness",  weight=0.25, scorer=...),
])

# Assemble the agent
agent = Agent(name="MyAgent", pipeline=pipeline, alignment=alignment)
result = agent.run("Calculate 42 * 7")
```

---

## Features

| Aspect | Traditional | I.QUEUE |
|--------|-----------|---------|
| **Skill Definition** | Text descriptions | `@skill` functions |
| **Rule Management** | Config files | `@rule` constraints |
| **Execution Flow** | Hidden in prompts | Explicit `Pipeline` stages |
| **Alignment** | Vague guidelines | Computable weighted formula |
| **Debugging** | Nearly impossible | Stage-by-stage tracking |

---

## Quick Start

```bash
git clone https://github.com/zhouyunhong2025-cloud/XIAOJIE.git
cd XIAOJIE/I.QUEUE
pip install -r requirements.txt
```

Run the example:

```bash
python example_agent.py
```

Sample output:

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

## Project Structure

```
I.QUEUE/
├── core/
│   ├── skill.py          # @skill decorator system
│   ├── rule.py           # @rule constraint engine
│   ├── pipeline.py       # Pipeline execution
│   ├── alignment.py      # Alignment formula calculation
│   └── agent.py          # Agent orchestrator
├── llm/
│   ├── openai_backend.py
│   └── anthropic_backend.py
├── memory.py             # Memory layer
├── example_agent.py      # Complete example
├── pyproject.toml        # Project configuration
├── requirements.txt      # Dependencies
└── README.md             # This file
```

---

## Core API

### `@skill` — Define a Skill

```python
@skill(name="translate", tags=["language"], priority=7)
def translate(text: str, target_lang: str = "en") -> str:
    """Translate text to target language."""
    return translated_text
```

### `@rule` — Define a Rule

```python
@rule(name="max_length", severity="warn", phase="post")
def check_length(output: str) -> tuple[bool, str]:
    ok = len(output) < 1000
    return ok, "Output exceeds 1000 characters"
```

### `Pipeline` — Define Execution Order

```python
pipeline = Pipeline([
    Phase("step1", fn1),
    Phase("step2", fn2, condition=lambda ctx: ctx.get("step1") is not None),
    Phase("step3", fn3),
])
```

### `AlignmentFormula` — Quantify Alignment

```python
formula = AlignmentFormula(
    dimensions=[
        AlignmentDimension("safety",  weight=0.5, scorer=safety_scorer,  floor=0.8),
        AlignmentDimension("quality", weight=0.5, scorer=quality_scorer, floor=0.6),
    ],
    threshold=0.70,
)
report = formula.evaluate(agent_output)
print(report)  # Visualized score bars
```

---

## Roadmap

- [ ] Support LLM backends (OpenAI / Anthropic)
- [ ] Auto-parse skill dependency graphs
- [ ] Alignment score history tracking
- [ ] YAML/JSON configuration export
- [ ] Web UI for Pipeline visualization
- [ ] Interactive tutorials

---

## License

MIT © 2025
