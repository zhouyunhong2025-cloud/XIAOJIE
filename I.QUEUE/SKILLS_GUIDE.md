# 🎨 I.QUEUE Skills & Cartridges System

## 什么是 Skills（技能）？

Skills 是预定义的、可复用的能力。每个 Skill 代表一种特定的功能。

## 什么是 Rules（规则）？

Rules 是约束，确保 Agent 的行为符合标准。

## 什么是 Cartridges（弹匣）？

Cartridges 是用户创建的配置文件，用来组装一个 Agent。就像把不同的方块放进去，系统就能运行。

---

## 🚀 三大预定义 Skills

### 1. Daily Summarizer（每日总结器）

**功能：** 把任何内容压缩成 5-10 条关键点

**使用场景：**
- ✓ 每天总结工作内容
- ✓ 浓缩邮件和消息
- ✓ 简化长文本
- ✓ 快速笔记整理

**配置文件：** `daily_summary.yaml`

```yaml
skills:
  - name: "daily_summarizer"
    config:
      summary_length: 7  # 保留 7 条要点
```

### 2. News Curator（新闻精选器）

**功能：** 从多个来源精选最有价值的内容

**使用场景：**
- ✓ 每日新闻精选
- ✓ 技术动态汇总
- ✓ 行业资讯筛选
- ✓ 学术论文推荐

**配置文件：** `news_curator.yaml`

```yaml
skills:
  - name: "news_curator"
    config:
      categories: ["technology", "business"]
      relevance_threshold: 0.7
      max_items: 10
```

### 3. Report Generator（报告生成器）

**功能：** 自动生成专业的日报/周报/月报

**使用场景：**
- ✓ 日报自动生成
- ✓ 周报/月报汇总
- ✓ 项目进度报告
- ✓ 工作汇总统计

**配置文件：** `report_generator.yaml`

```yaml
skills:
  - name: "report_generator"
    config:
      report_type: "daily"
      include_metrics: true
      include_next_steps: true
```

---

## 🏃 快速开始

### 步骤 1：复制模板

```bash
cp cartridges_template/daily_summary.yaml cartridges/my_bot.yaml
```

### 步骤 2：修改配置（可选）

编辑 `cartridges/my_bot.yaml`，调整参数

### 步骤 3：运行 Agent

```bash
python run.py --cartridge cartridges/my_bot.yaml --input "你的内容"
```

### 步骤 4：获取结果

系统会自动输出处理结果

---

## 📝 配置文件详解

每个 YAML 配置文件包含：

```yaml
name: "Agent 名称"                 # 你的 Agent 叫什么
description: "描述"               # 做什么的

skills:                            # 选择技能
  - name: "skill_name"
    config:
      param1: value1

rules:                             # 应用规则
  - name: "rule_name"

alignment:                         # 价值对齐（优先级）
  key1: 0.95
  key2: 0.85

llm:                               # 连接到 AI
  provider: "openai"
  model: "gpt-4"
```

---

## 🎯 高级用法：自定义 Skill

你也可以写自己的 Skill：

```python
# cartridges/my_custom_skill.py
from iqueue import Skill

class MyCustomSkill(Skill):
    name = "my_skill"
    
    def execute(self, content: str):
        # 你的逻辑
        return result
```

---

## 📚 项目结构

```
I.QUEUE/
├── skills/                    ← 预定义技能库
│   ├── daily_summarizer.py
│   ├── news_curator.py
│   └── report_generator.py
├── rules/                     ← 规则库
│   ├── safety_rule.py
│   └── format_rule.py
└── cartridges_template/       ← 用户 Agent 模板
    ├── daily_summary.yaml
    ├── news_curator.yaml
    └── report_generator.yaml
```

---

## 💡 提示

- 初学者：直接用 `.yaml` 配置文件，无需写代码
- 中级：自定义 Skill（写简单 Python）
- 高级：完全自定义 Agent 行为

---

## 🤔 常见问题

**Q: 我不会写代码，能用吗？**
A: 完全可以！直接编辑 YAML 文件即可，不需要写代码。

**Q: 能不能自己加技能？**
A: 可以！写一个继承 `Skill` 的 Python 类就行。

**Q: 支持中文吗？**
A: 完全支持，所有配置和输出都支持中文。
