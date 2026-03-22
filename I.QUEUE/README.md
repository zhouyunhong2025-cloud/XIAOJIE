# I.QUEUE Core Package

**Your AI Guardian. Fully Self-Configuring.**

[![Python](https://img.shields.io/badge/Python-3.10+-2ecc71?style=flat-square&logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-3498db?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-v0.1.0-e74c3c?style=flat-square)]()

---

## What You Get

Your AI automatically picks and configures:

| Element | What It Does |
|---------|-------------|
| **Memory** | How to remember context across conversations |
| **Skills** | What capabilities to use for your tasks |
| **Preferences** | How to behave and prioritize options |
| **Rules** | What boundaries and safety constraints to follow |

**You describe once. System designs everything.**

---

## Visual Showcase

![Core Concept](../docs/ScreenShot_2026-03-22_153838_603.png)

![Pre-Built Cartridges](../docs/ScreenShot_2026-03-22_153857_163.png)

---

## How It Works

1. **Input Your Need** → Natural language description
2. **AI Analyzes** → RequirementAnalyzer understands your need
3. **Recommends Config** → SkillRecommender selects best Memory/Skills/Preferences/Rules
4. **Generates Plan** → PlanGenerator creates markdown design document
5. **Deploy** → One-click execution with real-time monitoring

---

## Four Core Components

### 1. RequirementAnalyzer
Understands what you actually need from natural language.

```python
from requirement_analyzer import RequirementAnalyzer

analyzer = RequirementAnalyzer()
analysis = analyzer.analyze("Summarize my daily work")
# Returns: type, keywords, memory_needs, alignment_hints
```

### 2. SkillRecommender
Recommends optimal skills (local + open-source).

```python
from skill_recommender import SkillRecommender

recommender = SkillRecommender()
recommendations = recommender.recommend_skills(
    requirement_type="summary",
    include_opensource=True
)
# Returns: Priority-ranked skill suggestions
```

### 3. PlanGenerator
Creates complete design documents you can review.

```python
from plan_generator import PlanGenerator

generator = PlanGenerator()
plan = generator.generate_plan(
    requirement="Your need",
    analysis=analysis_result,
    skills=recommended_skills
)
# Returns: Markdown (human review) + YAML (machine execute)
```

### 4. AgentAutoDesigner
Orchestrates all components end-to-end.

```python
from agent_auto_designer import AgentAutoDesigner

designer = AgentAutoDesigner()
plan = designer.design_agent("Your natural language need")
# Returns: Complete design ready to deploy
```

---

## Pre-Built Skills

Three production-ready skills included:

| Skill | Purpose | Use Case |
|-------|---------|----------|
| **DailySummarizer** | Compress content into key points | Summarize work, news, articles |
| **NewsCurator** | Select best content from sources | Curate news, research, updates |
| **ReportGenerator** | Auto-generate professional reports | Daily/weekly/monthly reports |

---

## Quick Start

```bash
# Install with all features
pip install -r requirements.txt

# Run the intelligent designer
python quick_start.py "Summarize today's work"

# Or use in your code
from agent_auto_designer import AgentAutoDesigner
designer = AgentAutoDesigner()
plan = designer.design_agent("Your requirement")
print(plan.to_markdown())
```

---

## Project Structure

```
I.QUEUE/
├── agent_auto_designer.py        # 4-component orchestrator
├── requirement_analyzer.py       # Need analysis
├── skill_recommender.py          # Skill recommendations
├── plan_generator.py             # Design generation
├── skill.py                      # @skill decorator
├── rule.py                       # @rule constraint engine
├── base.py                       # Base classes
├── skills/                       # Pre-built skills library
├── rules/                        # Rules library
├── cartridges_template/          # YAML templates
├── web_server.py                 # FastAPI backend
├── web_ui/                       # Web interface
├── agent_monitor.py              # Desktop monitor panel
├── run.py                        # Launcher script
├── quick_start.py                # CLI quick start
├── pyproject.toml                # Project config
└── requirements.txt              # Dependencies
```

---

## Documentation

- [📖 Startup Guide](./STARTUP_GUIDE.md) — How to start (3 methods)
- [🛠️ Skills Guide](./SKILLS_GUIDE.md) — Write and use skills
- [⚙️ AutoDesigner Guide](./AGENT_AUTODESIGNER_GUIDE.md) — Detailed system explanation

---

## Features

✅ **Automatic Design** — Describe once, AI builds optimal config  
✅ **Web UI** — Visual designer with real-time preview  
✅ **Desktop Monitor** — Floating panel shows live execution  
✅ **One-Click Deploy** — From requirement to running agent  
✅ **Markdown Reports** — Review before approving  
✅ **YAML Config** — Export for reproducibility  

---

## Technology Stack

- **Python 3.10+** — Core language
- **FastAPI** — Web backend API
- **PyQt6** — Desktop monitoring
- **YAML** — Configuration format
- **HTML5 + CSS3 + JS** — Web frontend

---

## No Coding Required

Design agents with simple English. System handles:
- ✓ Analyzing your requirements
- ✓ Selecting best skills
- ✓ Configuring memory layer
- ✓ Setting preferences and rules
- ✓ Generating complete design
- ✓ Deploying and monitoring

---

## Get Started Now

```bash
# From repository root
cd I.QUEUE

# Choose your method
python run.py              # Interactive launcher
python quick_start.py "your need"  # CLI direct
python web_server.py       # Web UI only
```

Then describe what you need. AI does the rest.

---

## License

MIT © 2025
