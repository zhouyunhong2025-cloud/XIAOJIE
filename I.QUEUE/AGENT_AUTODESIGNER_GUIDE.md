# 🤖 Agent 自动设计系统使用指南

> **I.QUEUE 最大的创新**：让 Agent 自己根据你的需求，自动设计最优的 Agent 配置。
>
> 你只需要说一句话："帮我总结今天的工作"，剩下的交给系统！

## 🎯 核心理念

**从"手动配置"到"智能自动"**

在 Phase 6，我们提供了 Pre-built Skills 和 YAML 模板，已经大大降低了使用难度。

但现在，我们更进一步：

```
用户需求 → Agent 自动分析 → 推荐最优技能 → 生成完整方案 → 用户审批 → 一键启动
     (自然语言)           ↓              ↓              ↓          ↓        ↓
                    需求解析      Skill库匹配    Markdown文档  修改/确认  执行
```

This is truly **"傻瓜级"** (foolproof) - 非技术用户只需描述需求，系统搞定一切！

---

## 🚀 快速开始（3 步）

### 1️⃣ 定义你的需求

用自然语言描述你想要什么。系统支持以下三种主要场景：

```python
# 场景 1: 总结
"帮我总结今天的工作内容"
"压缩这些文档成关键要点"
"生成内容摘要"

# 场景 2: 精选和过滤
"为我精选最新的科技新闻"
"过滤相关内容"
"推荐商业信息"

# 场景 3: 报告生成
"生成我的周报"
"生成月度总结"
"自动生成日报"
```

### 2️⃣ 启动自动设计

```python
from agent_auto_designer import AgentAutoDesigner

# 创建设计师
designer = AgentAutoDesigner()

# 输入需求，自动生成设计方案
plan = designer.design_agent("帮我总结今天的工作内容")
```

系统会自动完成：
- 📊 需求分析
- ✨ 技能推荐（本地 + 开源）
- 🛡️ 规则配置
- 🧠 记忆设计
- 🎯 能力对齐

### 3️⃣ 审批并启动

```python
# 查看完整的设计方案
print(plan.to_markdown())

# 或者导出为文件便于审阅
designer.export_plan_markdown(plan, "my_agent_plan")

# 确认无误后，一键启动（待实现）
# designer.launch_agent(plan)
```

---

## 🧠 系统架构

AgentAutoDesigner 由四个核心组件组成：

### 1. RequirementAnalyzer（需求分析器）

**职责**: 理解用户的真实需求

```python
analyzer = RequirementAnalyzer()

analysis = analyzer.analyze("帮我总结今天的工作")

# 输出:
# {
#   primary_type: "summary",           # 主要类型
#   secondary_types: ["report"],       # 次要类型
#   keywords: ["总结", "工作"],        # 关键词
#   confidence: 0.95,                  # 分析信心度
#   memory_needs: {...},               # 推断的记忆需求
#   alignment_hints: {...},            # 对齐参数建议
#   recommendations: [...]             # 实施建议
# }
```

**支持的类型**:
- `summary` - 文本总结和压缩
- `curation` - 内容精选和过滤
- `report` - 报告生成

---

### 2. SkillRecommender（技能推荐器）

**职责**: 推荐最优的本地和开源技能

```python
recommender = SkillRecommender()

skills = recommender.recommend_skills(
    requirement_type="summary",
    secondary_types=[],
    keywords=["工作", "总结"],
    include_opensource=True
)

# 返回优先级排序的技能推荐列表
# [
#   SkillRecommendation(name="Daily Summarizer", priority=1, confidence=0.95),
#   SkillRecommendation(name="Text Analysis Suite", priority=2, confidence=0.60, url="..."),
#   ...
# ]
```

**技能来源**:
- 📦 **LOCAL** - I.QUEUE 内置技能
  - Daily Summarizer
  - News Curator
  - Report Generator
- 🐙 **GITHUB** - GitHub 开源项目
  - Text Analysis Suite
  - Content Enrichment
  - Semantic Search
- 🤗 **HUGGINGFACE** - HuggingFace 预训练模型
  - Advanced Summarization
- 📥 **PYPI** - Python 包
  - Data Visualization
  - Web Scraping

---

### 3. PlanGenerator（方案生成器）

**职责**: 生成用户可以审批的完整设计文档

```python
generator = PlanGenerator()

plan = generator.generate_plan(
    requirement="帮我总结今天的工作",
    analysis=analysis_result,
    skills=recommended_skills,
    rules=["content_safety", "format_consistency"],
    memory_config={...},
    alignment={...}
)

# 生成 Markdown 格式（用户审阅）
markdown_doc = plan.to_markdown()

# 生成 YAML 格式（机器执行）
yaml_config = plan.to_yaml_config()
```

**输出内容**:
- ✅ 完整的需求分析
- ✅ 推荐的技能组合（本地 + 开源）
- ✅ 应用规则
- ✅ 记忆配置
- ✅ 能力对齐参数
- ✅ 实施建议和替代方案
- ✅ 执行步骤指引

---

### 4. AgentAutoDesigner（主编排器）

**职责**: 整合所有组件，提供一站式服务

```python
designer = AgentAutoDesigner()

# 一行代码完成从需求到方案的全过程
plan = designer.design_agent("用户需求描述")
```

**6 步自动流程**:

```
1️⃣ 分析需求
   ↓
2️⃣ 推荐技能（本地 + 开源）
   ↓
3️⃣ 配置规则
   ↓
4️⃣ 设计记忆
   ↓
5️⃣ 设置对齐
   ↓
6️⃣ 生成文档
```

---

## 📋 详细使用例子

### 例 1: 总结 Agent

**用户需求**:
```
"帮我总结今天的工作内容"
```

**系统自动设计**:

```
📊 需求分析:
   主要类型: SUMMARY (信心 95%)
   辅助类型: REPORT
   关键词: 总结、工作
   
✨ 推荐技能:
   1. Daily Summarizer (本地, P1)
   2. Report Generator (本地, P2)
   3. Advanced Summarization (HF, P2)
   4. Text Analysis Suite (GitHub, P2)
   
🛡️ 应用规则:
   • Content Safety (确保安全)
   • Format Consistency (保证风格一致)
   
🧠 记忆配置:
   • retention_days: 7
   • track_patterns: 启用
   • learn_style: 启用
   
🎯 能力对齐:
   • clarity: 95%      (清晰度)
   • conciseness: 98%  (简洁性)
   • completeness: 85% (完整性)
```

**生成的设计文档**:
查看 [plan_1.md](mnt/user-data/outputs/agent_plans/plan_1.md)

---

### 例 2: 新闻精选 Agent

**用户需求**:
```
"为我精选最新的科技和商业新闻"
```

**系统自动设计**:

```
📊 需求分析:
   主要类型: CURATION (信心 92%)
   关键词: 精选、新闻、科技、商业
   
✨ 推荐技能:
   1. News Curator (本地, P1)
      - categories: [technology, business]
      - relevance_threshold: 0.7
   2. Web Scraping (PyPI, P3)
   3. Content Enrichment (GitHub, P2)
   4. Semantic Search (GitHub, P3)
   
🧠 记忆配置:
   • retention_days: 30
   • track_preferences: 启用
   • learn_interests: 启用
   
🎯 能力对齐:
   • relevance: 95%   (相关性)
   • timeliness: 90%  (及时性)
   • uniqueness: 85%  (独特性)
```

**生成的设计文档**:
查看 [plan_2.md](mnt/user-data/outputs/agent_plans/plan_2.md)

---

### 例 3: 周报生成 Agent

**用户需求**:
```
"生成我的周报"
```

**系统自动设计**:

```
📊 需求分析:
   主要类型: REPORT (信心 93%)
   关键词: 周报、生成
   
✨ 推荐技能:
   1. Report Generator (本地, P1)
      - report_type: weekly
      - include_metrics: true
   2. Data Visualization (PyPI, P2)
   3. Content Enrichment (GitHub, P2)
   
🧠 记忆配置:
   • retention_days: 90
   • track_history: 启用
   • archive_reports: 启用
   
🎯 能力对齐:
   • professionalism: 98% (专业性)
   • clarity: 95%         (清晰度)
   • completeness: 90%    (完整性)
```

**生成的设计文档**:
查看 [plan_3.md](mnt/user-data/outputs/agent_plans/plan_3.md)

---

## 🛠️ 高级使用

### 自定义技能配置

```python
# 系统推荐的 skill
skill = recommendations[0]

# 修改配置
custom_config = {
    "summary_length": 10,      # 改为 10 个要点
    "auto_save": False,        # 关闭自动保存
}

customized = recommender.customize_config(skill, custom_config)
```

### 查看替代方案

```python
plan = designer.design_agent("帮我总结工作")

# 查看替代方案
print(plan.alternatives)
# {
#   "总结长度": ["简要版", "标准版", "详细版"],
#   "更新频率": ["每日一次", "每周一次", "按需更新"]
# }
```

### 导出为不同格式

```python
# Markdown - 人类审阅
designer.export_plan_markdown(plan, "my_plan")
# → /workspaces/XIAOJIE/I.QUEUE/mnt/user-data/outputs/agent_plans/my_plan.md

# YAML - 自动执行
designer.export_plan_yaml(plan, "my_plan_config")
# → /workspaces/XIAOJIE/I.QUEUE/mnt/user-data/outputs/agent_configs/my_plan_config.yaml
```

---

## 🔌 与现有系统的集成

AgentAutoDesigner 设计时考虑了与 I.QUEUE 现有系统的无缝集成：

### 与 Skills 系统集成
```
AutoDesigner 推荐的 Skills
          ↓
    从 I.QUEUE/skills/ 加载
          ↓
    与 Skill 基类兼容
          ↓
    即插即用
```

### 与 Rules 系统集成
```
AutoDesigner 推荐的 Rules
          ↓
    从 I.QUEUE/rules/ 加载
          ↓
    在 Agent 执行时应用
          ↓
    确保输出安全和一致
```

### 与 Memory 系统集成
```
AutoDesigner 配置的 Memory
          ↓
    自动创建记忆系统
          ↓
    Agent 持续学习和改进
          ↓
    下次推荐更加精准
```

### 与 Alignment 系统集成
```
AutoDesigner 设置的对齐
          ↓
    定义 Agent 的优先级
          ↓
    指导所有决策
          ↓
    确保行为一致
```

---

## 📊 决策过程（技术细节）

### 需求分析算法

```
输入: 自然语言需求
      ↓
1. 关键词匹配 - 与类型库比对
   summary:  ["总结", "汇总", "摘要", ...]
   curation: ["精选", "推荐", "过滤", ...]
   report:   ["报告", "日报", "周报", ...]
      ↓
2. 类型识别 - 选择得分最高的类型
      ↓
3. 次要类型检测 - 发现补充类型
      ↓
4. 关键词提取 - 用于后续精细化
      ↓
5. 记忆需求推断 - 从关键词猜测
      ↓
6. 对齐建议 - 根据需求调整优先级
      ↓
输出: RequirementAnalysis 对象
```

### Skill 推荐算法

```
输入: 需求分析结果
      ↓
1. 获取必需的本地 Skills
   summary → Daily Summarizer
   curation → News Curator
   report → Report Generator
      ↓
2. 查找辅助 Skills（次要类型）
      ↓
3. 搜索开源替代方案
   - GitHub 生态 (NLP, ML)
   - HuggingFace 模型库
   - PyPI 实用包
      ↓
4. 计算匹配分数（基于关键词）
      ↓
5. 按优先级排序
      ↓
6. 返回推荐列表 (本地 P1 → 开源 P2+)
      ↓
输出: SkillRecommendation 列表
```

---

## 💡 使用建议

### 什么时候使用 AutoDesigner?

✅ **使用**:
- 你是非技术用户
- 你不确定需要哪些 Skills
- 你想快速启动一个新 Agent
- 你想看看系统推荐什么

❌ **不用**:
- 你已经知道确切需要什么
- 你想手动微调每个参数
- 你在做 Agent 定制开发

### 最佳实践

1. **清晰描述需求**
   ```
   ✅ 好: "帮我总结今天会议的关键点"
   ❌ 差: "总结"
   ```

2. **查看推荐后再启动**
   ```
   适当修改配置，确保符合预期
   不要盲目使用默认配置
   ```

3. **监测第一次运行**
   ```
   查看输出是否符合预期
   如果不满意，调整参数再试
   记录效果，帮助系统学习
   ```

4. **定期评估和改进**
   ```
   每周检查 Agent 的输出质量
   收集反馈信息
   使用改进的数据重新设计 Agent
   ```

---

## 🚀 下一步计划

### 已完成（✅）
- [x] 需求分析器
- [x] Skill 推荐器
- [x] 方案生成器
- [x] 主编排器
- [x] 设计文档生成
- [x] 3 个样本方案

### 进行中（⏳）
- [ ] 用户界面 (CLI / Web)
- [ ] 一键启动功能
- [ ] 实时监测面板
- [ ] 反馈学习系统

### 规划中（🔮）
- [ ] 多语言支持
- [ ] 社区技能库（Awesome Lists）
- [ ] Agent 性能评分
- [ ] 自动优化建议
- [ ] 协作设计（团队工作）

---

## 📞 获取帮助

有问题或建议？

1. 查看 [SKILLS_GUIDE.md](SKILLS_GUIDE.md) - 了解基础 Skills
2. 查看 [生成的方案文档](mnt/user-data/outputs/agent_plans/) - 学习例子
3. 检查日志 - 查看设计过程
4. 反馈给我们 - 帮助改进系统

---

## 🎉 总结

```
从 Phase 6: "给我 YAML，非对程序员可用"
到 Phase 7: "说一句话，系统自动设计一切"

这是真正的革新！

不再有技术障碍。
不再有复杂配置。
只需描述，系统搞定。

这才是 "傻瓜级" ✨
```

**Now go design your perfect Agent! 🚀**

---

*Generated by I.QUEUE AgentAutoDesigner System*
*Last Updated: 2026-03-22*
