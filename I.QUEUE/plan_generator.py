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
        output.append("# 🤖 Agent 智能设计方案")
        output.append("")
        output.append(f"**生成时间**: {datetime.fromisoformat(self.created_at).strftime('%Y-%m-%d %H:%M:%S')}")
        output.append(f"**方案ID**: `plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}`")
        output.append("")
        
        # 用户需求
        output.append("## 📋 用户需求")
        output.append("━━━━━━━━━━━━━━━━━━━")
        output.append(f"> {self.requirement}")
        output.append("")
        
        # 需求分析
        output.append("## 🔍 需求分析")
        output.append("━━━━━━━━━━━━━━━━━━━")
        
        if self.analysis:
            output.append(f"**主要类型**: `{self.analysis.primary_type.upper()}`")
            output.append(f"**分析信心**: {self.analysis.confidence:.0%}")
            
            if self.analysis.secondary_types:
                output.append(f"**辅助类型**: {', '.join([f'`{t}`' for t in self.analysis.secondary_types])}")
            
            if self.analysis.keywords:
                output.append(f"**关键词**: {', '.join(self.analysis.keywords[:5])}")
        
        output.append("")
        
        # 推荐的技能
        output.append("## ✨ 推荐技能组合")
        output.append("━━━━━━━━━━━━━━━━━━━")
        
        local_skills = [s for s in self.skills if s.source == SkillSource.LOCAL]
        opensource_skills = [s for s in self.skills if s.source != SkillSource.LOCAL]
        
        if local_skills:
            output.append("### 📦 核心技能（本地）")
            output.append("")
            
            for idx, skill in enumerate(local_skills, 1):
                output.append(f"**{idx}. {skill.name}**")
                output.append(f"- {skill.description}")
                output.append(f"- 优先级: P{skill.priority} | 信心: {skill.confidence:.0%}")
                
                if skill.config:
                    output.append("- 推荐配置:")
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
            output.append("### 🚀 高级功能（开源推荐）")
            output.append("")
            output.append("> 这些是可选的开源项目，可以进一步增强 Agent 的能力。")
            output.append("")
            
            for idx, skill in enumerate(opensource_skills, 1):
                source_emoji = {
                    SkillSource.GITHUB: "🐙",
                    SkillSource.HUGGINGFACE: "🤗",
                    SkillSource.PYPI: "📥"
                }.get(skill.source, "🔧")
                
                output.append(f"**{idx}. {source_emoji} {skill.name}** ({skill.source.value})")
                output.append(f"- {skill.description}")
                output.append(f"- 优先级: P{skill.priority} | 匹配度: {skill.confidence:.0%}")
                
                if skill.url:
                    output.append(f"- 🔗 项目地址: [{skill.url}]({skill.url})")
                
                output.append("")
        
        # 规则配置
        if self.rules:
            output.append("## 🛡️ 应用规则")
            output.append("━━━━━━━━━━━━━━━━━━━")
            
            for rule in self.rules:
                output.append(f"- `{rule}`")
            
            output.append("")
        
        # 记忆配置
        if self.memory_config:
            output.append("## 🧠 记忆配置")
            output.append("━━━━━━━━━━━━━━━━━━━")
            
            for key, value in self.memory_config.items():
                if isinstance(value, bool):
                    output.append(f"- **{key}**: {'✓ 启用' if value else '✗ 禁用'}")
                else:
                    output.append(f"- **{key}**: {value}")
            
            output.append("")
        
        # 对齐参数
        if self.alignment:
            output.append("## 🎯 能力对齐")
            output.append("━━━━━━━━━━━━━━━━━━━")
            output.append("")
            output.append("这些参数定义了 Agent 在不同维度上的优先级:")
            output.append("")
            
            for key, value in sorted(self.alignment.items()):
                bar_length = int(value * 10)
                bar = "█" * bar_length + "░" * (10 - bar_length)
                output.append(f"- **{key}**: [{bar}] {value:.0%}")
            
            output.append("")
        
        # 实施建议
        output.append("## 💡 实施建议")
        output.append("━━━━━━━━━━━━━━━━━━━")
        
        if self.analysis and self.analysis.recommendations:
            for rec in self.analysis.recommendations:
                output.append(f"- {rec}")
        
        output.append("")
        
        # 替代方案
        if self.alternatives:
            output.append("## 🔄 替代方案")
            output.append("━━━━━━━━━━━━━━━━━━━")
            
            for scenario, options in self.alternatives.items():
                output.append(f"**{scenario}**:")
                for option in options:
                    output.append(f"- {option}")
            
            output.append("")
        
        # 执行步骤
        output.append("## 🚀 下一步执行")
        output.append("━━━━━━━━━━━━━━━━━━━")
        output.append("")
        output.append("1. **检查**: 仔细阅读本方案，确认所有配置符合预期")
        output.append("2. **修改**: 如需要，可以修改任何配置项")
        output.append("3. **确认**: 确认无误后，按下**一键启动**按钮")
        output.append("4. **运行**: Agent 会自动启动并开始处理")
        output.append("5. **监测**: 查看实时输出日志，确保一切正常")
        output.append("")
        
        # 快速参考
        output.append("## 📚 快速参考")
        output.append("━━━━━━━━━━━━━━━━━━━")
        output.append("")
        output.append(f"**技能总数**: {len(self.skills)} 个")
        output.append(f"**本地技能**: {len(local_skills)} 个 | **开源推荐**: {len(opensource_skills)} 个")
        output.append(f"**规则数**: {len(self.rules)} 个")
        output.append(f"**记忆配置**: {len(self.memory_config)} 项")
        output.append(f"**对齐维度**: {len(self.alignment)} 个")
        
        output.append("")
        output.append("---")
        output.append("")
        output.append("*这个方案由 I.QUEUE Agent 智能设计系统自动生成。*")
        
        return "\n".join(output)
    
    def to_yaml_config(self) -> str:
        """生成可执行的 YAML 配置"""
        output = []
        
        output.append("# Agent 配置文件")
        output.append("# 自动生成，请勿手动修改")
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
            analysis: 需求分析结果
            skills: 推荐的技能列表
            rules: 应用的规则列表
            memory_config: 记忆配置
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
        
        # 生成替代方案
        plan.alternatives = self._generate_alternatives(analysis)
        
        return plan
    
    def _generate_alternatives(self, analysis: RequirementAnalysis) -> Dict[str, List[str]]:
        """生成替代方案"""
        alternatives = {}
        
        if analysis.primary_type == "summary":
            alternatives["总结长度"] = [
                "简要版 (3-5 项要点)",
                "标准版 (7-10 项要点)",
                "详细版 (20+ 项要点)"
            ]
            alternatives["更新频率"] = [
                "每日一次",
                "每周一次",
                "按需更新"
            ]
        
        elif analysis.primary_type == "curation":
            alternatives["内容来源"] = [
                "仅本地数据",
                "互联网新闻源",
                "社交媒体",
                "多源聚合"
            ]
            alternatives["推荐算法"] = [
                "关键词匹配",
                "语义相似度",
                "协作过滤",
                "混合算法"
            ]
        
        elif analysis.primary_type == "report":
            alternatives["报告风格"] = [
                "简明版",
                "标准版",
                "详细分析版"
            ]
            alternatives["包含元素"] = [
                "仅成就",
                "成就+挑战",
                "成就+挑战+后续计划",
                "加上关键指标"
            ]
        
        return alternatives
