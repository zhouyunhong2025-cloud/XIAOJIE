# Skills & Cartridges System

## What are Skills?

Skills are pre-defined, reusable capabilities. Each Skill represents a specific function.

## What are Rules?

Rules are constraints that ensure Agent behavior meets standards.

## What are Cartridges?

Cartridges are user-created config files to assemble an Agent. Like placing different blocks together to make the system run.

---

## 🚀 Three Pre-Built Skills

### 1. Daily Summarizer

**Function:** Compress any content into 5-10 key points

**Use cases:**
- ✓ Summarize daily work
- ✓ Condense emails and messages
- ✓ Simplify long texts
- ✓ Quick note organization

**Config file:** `daily_summary.yaml`

```yaml
skills:
  - name: "daily_summarizer"
    config:
      summary_length: 7  # Keep 7 key points
```

### 2. News Curator

**Function:** Select most valuable content from multiple sources

**Use cases:**
- ✓ Daily news highlights
- ✓ Tech updates summary
- ✓ Industry news filtering
- ✓ Academic paper recommendations

**Config file:** `news_curator.yaml`

```yaml
skills:
  - name: "news_curator"
    config:
      categories: ["technology", "business"]
      relevance_threshold: 0.7
      max_items: 10
```

### 3. Report Generator

**Function:** Auto-generate professional daily/weekly/monthly reports

**Use cases:**
- ✓ Auto daily reports
- ✓ Weekly/monthly summaries
- ✓ Project progress reports
- ✓ Work summary statistics

**Config file:** `report_generator.yaml`

```yaml
skills:
  - name: "report_generator"
    config:
      report_type: "daily"
      include_metrics: true
      include_next_steps: true
```

---

## 🏃 Quick Start

### Step 1: Copy Template

```bash
cp cartridges_template/daily_summary.yaml cartridges/my_bot.yaml
```

### Step 2: Edit Config (Optional)

Edit `cartridges/my_bot.yaml` to adjust parameters

### Step 3: Run Agent

```bash
python run.py --cartridge cartridges/my_bot.yaml --input "your content"
```

### Step 4: Get Results

System automatically outputs results

---

## 📝 Config File Details

Each YAML config file contains:

```yaml
name: "Agent Name"                    # What it's called
description: "Description"            # What it does

skills:                               # Select skills
  - name: "skill_name"
    config:
      param1: value1

rules:                                # Apply rules
  - name: "rule_name"

alignment:                            # Value alignment (priority)
  key1: 0.95
  key2: 0.85

llm:                                  # Connect to AI
  provider: "openai"
  model: "gpt-4"
```

---

## 🎯 Advanced: Custom Skills

You can write your own Skills:

```python
# cartridges/my_custom_skill.py
from iqueue import Skill

class MyCustomSkill(Skill):
    name = "my_skill"
    
    def execute(self, content: str):
        # Your logic here
        return result
```

---

## 📚 Project Structure

```
I.QUEUE/
├── skills/                    ← Pre-built skill library
│   ├── daily_summarizer.py
│   ├── news_curator.py
│   └── report_generator.py
├── rules/                     ← Rule library
│   ├── safety_rule.py
│   └── format_rule.py
└── cartridges_template/       ← User Agent templates
    ├── daily_summary.yaml
    ├── news_curator.yaml
    └── report_generator.yaml
```

---

## 💡 Tips

- **Beginners:** Use `.yaml` files directly, no code needed
- **Intermediate:** Write custom Skills (simple Python)
- **Advanced:** Full custom Agent behavior

---

## 🤔 FAQ

**Q: I don't know how to code, can I still use this?**
A: Absolutely! Just edit YAML files directly, no code required.

**Q: Can I add my own skills?**
A: Yes! Write a Python class that inherits `Skill`.

**Q: Does it support languages other than English?**
A: Yes! All config and output fully support multiple languages.
