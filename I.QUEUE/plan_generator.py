"""
计划生成器 - 生成 Agent 设计文档
根据分析和推荐，生成用户可以审核的完整设计文档
"""

from typing import List, Dict, Any
from datetime import datetime
from requirement_analyzer import RequirementAnalysis
from skill_recommender import SkillRecommendation, SkillSource


class AgentDesignPlan:
    """Agent 设计方案"""
    
    def __init__(self):
        self.created_at = datetime.now().isoformat()
        self.requirement: str = ""
        self.analysis: RequirementAnalysis = None
        self.skills: List[SkillRecommendation] = []
        self.rules: List[str] = []
        self.memory_config: Dict[str, Any] = {}
        self.alignment: Dict[str, float] = {}
        self.notes: List[str] = []
        self.alternatives: Dict[str, List[str]] = {}
    
    def to_markdown(self) -> str:
        """生成 Markdown 格式的设计文档"""
        output = []
        
        # 标题和基本信息
        output.append("# 🤖 Agent Intelligent Design Plan")
        output.append("")
        output.append(f"**Generated Time**: {datetime.fromisoformat(self.created_at).strftime('%Y-%m-%d %H:%M:%S')}")
        output.append(f"**Plan ID**: `plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}`")
        output.append("")
        
        # Requirement
        output.append("## 📋 Requirement")
        output.append("━━━━━━━━━━━━━━━━━━━")
        output.append(f"> {self.requirement}")
        output.append("")
        
        # Requirement Analysis
        output.append("## 🔍 Requirement Analysis")
        output.append("━━━━━━━━━━━━━━━━━━━")
        
        if self.analysis:
            output.append(f"**Primary Type**: `{self.analysis.primary_type.upper()}`")
            output.append(f"**Analysis Confidence**: {self.analysis.confidence:.0%}")
            
            if self.analysis.secondary_types:
                output.append(f"**Secondary Type**: {', '.join([f'`{t}`' for t in self.analysis.secondary_types])}")
            
            if self.analysis.keywords:
                output.append(f"**Keywords**: {', '.join(self.analysis.keywords[:5])}")
        
        output.append("")
        
        # 推荐的技能
        output.append("## ✨ Recommended Skill Combination")
        output.append("━━━━━━━━━━━━━━━━━━━")
        
        local_skills = [s for s in self.skills if s.source == SkillSource.LOCAL]
        opensource_skills = [s for s in self.skills if s.source != SkillSource.LOCAL]
        
        if local_skills:
            output.append("### 📦 Core Skills (Local)")
            output.append("")
            
            for idx, skill in enumerate(local_skills, 1):
                output.append(f"**{idx}. {skill.name}**")
                output.append(f"- {skill.description}")
                output.append(f"- Priority: P{skill.priority} | Confidence: {skill.confidence:.0%}")
                
                if skill.config:
                    output.append("- Recommended Config:")
                    for key, value in skill.config.items():
                        if isinstance(value, dict):
                            output.append(f"  - `{key}`:")
                            for k, v in value.items():
                                output.append(f"    - `{k}`: {v}")
                        elif isinstance(value, list):
                            output.append(f"  - `{key}`: {', '.join(str(v) for v in value)}")
                        else:
                            output.append(f"  - `{key}`: {value}")
                
                output.append("")
        
        if opensource_skills:
            output.append("### 🚀 Advanced Features (Open-source Recommendations)")
            output.append("")
            output.append("> These are optional open-source projects that can further enhance Agent capabilities.")
            output.append("")
            
            for idx, skill in enumerate(opensource_skills, 1):
                source_emoji = {
                    SkillSource.GITHUB: "🐙",
                    SkillSource.HUGGINGFACE: "🤗",
                    SkillSource.PYPI: "📥"
                }.get(skill.source, "🔧")
                
                output.append(f"**{idx}. {source_emoji} {skill.name}** ({skill.source.value})")
                output.append(f"- {skill.description}")
                output.append(f"- Priority: P{skill.priority} | 匹配度: {skill.confidence:.0%}")
                
                if skill.url:
                    output.append(f"- 🔗 Project URL: [{skill.url}]({skill.url})")
                
                output.append("")
        
        # 规则配置
        if self.rules:
            output.append("## 🛡️ Rules")
            output.append("━━━━━━━━━━━━━━━━━━━")
            
            for rule in self.rules:
                output.append(f"- `{rule}`")
            
            output.append("")
        
        # Memory Configuration
        if self.memory_config:
            output.append("## 🧠 Memory Configuration")
            output.append("━━━━━━━━━━━━━━━━━━━")
            
            for key, value in self.memory_config.items():
                if isinstance(value, bool):
                    output.append(f"- **{key}**: {'✓ Enabled' if value else '✗ Disabled'}")
                else:
                    output.append(f"- **{key}**: {value}")
            
            output.append("")
        
        # 对齐参数
        if self.alignment:
            output.append("## 🎯 Capability Alignment")
            output.append("━━━━━━━━━━━━━━━━━━━")
            output.append("")
            output.append("这些参数定义了 Agent 在不同维度上的Priority:")
            output.append("")
            
            for key, value in sorted(self.alignment.items()):
                bar_length = int(value * 10)
                bar = "█" * bar_length + "░" * (10 - bar_length)
                output.append(f"- **{key}**: [{bar}] {value:.0%}")
            
            output.append("")
        
        # Implementation Recommendations
        output.append("## 💡 Implementation Recommendations")
        output.append("━━━━━━━━━━━━━━━━━━━")
        
        if self.analysis and self.analysis.recommendations:
            for rec in self.analysis.recommendations:
                output.append(f"- {rec}")
        
        output.append("")
        
        # Alternatives
        if self.alternatives:
            output.append("## 🔄 Alternatives")
            output.append("━━━━━━━━━━━━━━━━━━━")
            
            for scenario, options in self.alternatives.items():
                output.append(f"**{scenario}**:")
                for option in options:
                    output.append(f"- {option}")
            
            output.append("")
        
        # 执行步骤
        output.append("## 🚀 Next Steps")
        output.append("━━━━━━━━━━━━━━━━━━━")
        output.append("")
        output.append("1. **Review**: Carefully read this plan and confirm all settings meet expectations")
        output.append("2. **Modify**: 如需要，可以Modify任何配置items")
        output.append("3. **Confirm**: Confirm无误后，按下**One-Click Deploy**button")
        output.append("4. **Run**: Agent will automatically start and begin processing")
        output.append("5. **Monitor**: View real-time output logs to ensure everything is working")
        output.append("")
        
        # Quick Reference
        output.append("## 📚 Quick Reference")
        output.append("━━━━━━━━━━━━━━━━━━━")
        output.append("")
        output.append(f"**Total Skills**: {len(self.skills)} items")
        output.append(f"**Local Skills**: {len(local_skills)} items | **Open-source Recommendations**: {len(opensource_skills)} items")
        output.append(f"**Number of Rules**: {len(self.rules)} items")
        output.append(f"**Memory Configuration**: {len(self.memory_config)} items")
        output.append(f"**Alignment Dimensions**: {len(self.alignment)} items")
        
        output.append("")
        output.append("---")
        output.append("")
        output.append("*这items方案由 I.QUEUE Agent 智能设计系统自动生成。*")
        
        return "\n".join(output)
    
    def to_yaml_config(self) -> str:
        """生成可执行的 YAML 配置"""
        output = []
        
        output.append("# Agent 配置文件")
        output.append("# 自动生成，请勿手动Modify")
        output.append("")
        
        output.append("metadata:")
        output.append(f"  created_at: '{self.created_at}'")
        output.append(f"  requirement: '{self.requirement}'")
        output.append("")
        
        output.append("skills:")
        for skill in self.skills:
            if skill.source == SkillSource.LOCAL:
                output.append(f"  - name: {skill.name}")
                output.append(f"    enabled: true")
                
                if skill.config:
                    output.append(f"    config:")
                    for key, value in skill.config.items():
                        output.append(f"      {key}: {self._yaml_value(value)}")
        
        output.append("")
        
        if self.rules:
            output.append("rules:")
            for rule in self.rules:
                output.append(f"  - {rule}")
            output.append("")
        
        if self.memory_config:
            output.append("memory:")
            for key, value in self.memory_config.items():
                output.append(f"  {key}: {self._yaml_value(value)}")
            output.append("")
        
        if self.alignment:
            output.append("alignment:")
            for key, value in self.alignment.items():
                output.append(f"  {key}: {value:.2f}")
        
        return "\n".join(output)
    
    @staticmethod
    def _yaml_value(value: Any) -> str:
        """将 Python 值转换为 YAML 格式"""
        if isinstance(value, bool):
            return "true" if value else "false"
        elif isinstance(value, (list, tuple)):
            return "[" + ", ".join(str(v) for v in value) + "]"
        elif isinstance(value, str):
            return f"'{value}'"
        else:
            return str(value)


class PlanGenerator:
    """设计方案生成器"""
    
    def generate_plan(self,
                     requirement: str,
                     analysis: RequirementAnalysis,
                     skills: List[SkillRecommendation],
                     rules: List[str],
                     memory_config: Dict[str, Any],
                     alignment: Dict[str, float]) -> AgentDesignPlan:
        """
        生成完整的 Agent 设计计划
        
        Args:
            requirement: 用户原始需求
            analysis: Requirement Analysis Result
            skills: List of recommended skills
            rules: 应用的规则列表
            memory_config: Memory Configuration
            alignment: 对齐参数
            
        Returns:
            完整的 AgentDesignPlan
        """
        plan = AgentDesignPlan()
        
        plan.requirement = requirement
        plan.analysis = analysis
        plan.skills = skills
        plan.rules = rules
        plan.memory_config = memory_config
        plan.alignment = alignment
        
        # 生成Alternatives
        plan.alternatives = self._generate_alternatives(analysis)
        
        return plan
    
    def _generate_alternatives(self, analysis: RequirementAnalysis) -> Dict[str, List[str]]:
        """生成Alternatives"""
        alternatives = {}
        
        if analysis.primary_type == "summary":
            alternatives["Summary Length"] = [
                "Brief (3-5 items要点)",
                "Standard (7-10 items要点)",
                "Detailed (20+ items要点)"
            ]
            alternatives["Update Frequency"] = [
                "Daily",
                "Weekly",
                "On Demand"
            ]
        
        elif analysis.primary_type == "curation":
            alternatives["内容Source"] = [
                "仅本地数据",
                "互联网新闻源",
                "社交媒体",
                "多源聚合"
            ]
            alternatives["推荐算法"] = [
                "Keywords匹配",
                "语义相似度",
                "协作过滤",
                "混合算法"
            ]
        
        elif analysis.primary_type == "report":
            alternatives["报告风格"] = [
                "简明版",
                "Standard",
                "详细分析版"
            ]
            alternatives["包含元素"] = [
                "仅成就",
                "成就+挑战",
                "成就+挑战+后续计划",
                "加上关键指标"
            ]
        
        return alternatives
