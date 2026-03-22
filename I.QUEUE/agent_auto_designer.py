"""
Agent 自动设计系统 - AgentAutoDesigner
这是 I.QUEUE 最核心的创新：让 Agent 自动根据需求设计最优的 Agent 配置
"""

from typing import Dict, Any, Optional
from requirement_analyzer import RequirementAnalyzer, RequirementAnalysis
from skill_recommender import SkillRecommender, SkillRecommendation
from plan_generator import PlanGenerator, AgentDesignPlan


class AgentAutoDesigner:
    """
    智能 Agent 设计系统的大脑
    
    工作流程:
    1. 用户提供需求 → 2. 分析需求 → 3. 推荐技能 → 4. 生成方案文档
    5. 用户审核 → 6. 用户修改 → 7. 确认执行 → 8. 自动启动 Agent
    """
    
    def __init__(self):
        self.requirement_analyzer = RequirementAnalyzer()
        self.skill_recommender = SkillRecommender()
        self.plan_generator = PlanGenerator()
        
        # 预设的规则组合
        self.RULE_TEMPLATES = {
            "summary": ["content_safety", "format_consistency"],
            "curation": ["content_safety", "format_consistency"],
            "report": ["content_safety", "format_consistency"]
        }
        
        # 预设的对齐参数
        self.ALIGNMENT_TEMPLATES = {
            "summary": {
                "clarity": 0.95,
                "conciseness": 0.98,
                "completeness": 0.85,
                "accuracy": 0.92
            },
            "curation": {
                "relevance": 0.95,
                "timeliness": 0.90,
                "uniqueness": 0.85,
                "diversity": 0.80
            },
            "report": {
                "professionalism": 0.98,
                "clarity": 0.95,
                "completeness": 0.90,
                "actionability": 0.85
            }
        }
    
    def design_agent(self, user_requirement: str) -> AgentDesignPlan:
        """
        一步到位：从需求到完整的 Agent 设计方案
        
        这是 I.QUEUE 的核心创新！
        
        Args:
            user_requirement: 用户的自然语言需求
                例如: "帮我总结今天的工作"
                     "精选科技和商业新闻"
                     "生成我的周报"
            
        Returns:
            完整可执行的 Agent 设计方案
        """
        
        print("\n🚀 开始 Agent 智能设计...")
        print("━" * 50)
        
        # 步骤 1: 分析需求
        print("\n📊 第 1 步: 深度分析需求...")
        analysis = self._analyze_requirement(user_requirement)
        print(self.requirement_analyzer.explain_analysis(analysis))
        
        # 步骤 2: 推荐技能
        print("\n✨ 第 2 步: 推荐最优技能...")
        skills = self._recommend_skills(analysis)
        print(self.skill_recommender.format_recommendations(skills))
        
        # 步骤 3: 设置规则
        print("\n🛡️  第 3 步: 配置应用规则...")
        rules = self._setup_rules(analysis.primary_type)
        print(self._format_rules(rules))
        
        # 步骤 4: 设计记忆
        print("\n🧠 第 4 步: 配置记忆系统...")
        memory_config = self._design_memory(analysis)
        print(self._format_memory(memory_config))
        
        # 步骤 5: 设置对齐
        print("\n🎯 第 5 步: 设置能力对齐...")
        alignment = self._compute_alignment(analysis)
        print(self._format_alignment(alignment))
        
        # 步骤 6: 生成设计文档
        print("\n📋 第 6 步: 生成设计文档...")
        plan = self.plan_generator.generate_plan(
            requirement=user_requirement,
            analysis=analysis,
            skills=skills,
            rules=rules,
            memory_config=memory_config,
            alignment=alignment
        )
        
        print("\n✅ 设计完成！")
        print("━" * 50)
        
        return plan
    
    def _analyze_requirement(self, requirement: str) -> RequirementAnalysis:
        """分析用户需求"""
        return self.requirement_analyzer.analyze(requirement)
    
    def _recommend_skills(self, analysis: RequirementAnalysis) -> list:
        """推荐技能"""
        skills = self.skill_recommender.recommend_skills(
            requirement_type=analysis.primary_type,
            secondary_types=analysis.secondary_types,
            keywords=analysis.keywords,
            include_opensource=True
        )
        return skills
    
    def _setup_rules(self, requirement_type: str) -> list:
        """设置规则"""
        return self.RULE_TEMPLATES.get(requirement_type, ["content_safety"])
    
    def _design_memory(self, analysis: RequirementAnalysis) -> Dict[str, Any]:
        """设计记忆配置"""
        # 从分析结果中提取记忆需求
        memory = analysis.memory_needs.copy()
        
        # 添加通用配置
        memory["enabled"] = True
        memory["auto_save"] = True
        memory["version"] = 1
        
        return memory
    
    def _compute_alignment(self, analysis: RequirementAnalysis) -> Dict[str, float]:
        """计算对齐参数"""
        # 从模板获取基础对齐参数
        alignment = self.ALIGNMENT_TEMPLATES.get(
            analysis.primary_type,
            {"quality": 0.90}
        )
        
        # 根据关键词调整
        if any(w in analysis.keywords for w in ["精准", "准确", "accurate"]):
            alignment["accuracy"] = min(alignment.get("accuracy", 0.9) + 0.05, 1.0)
        
        if any(w in analysis.keywords for w in ["快速", "快", "fast"]):
            alignment["speed"] = 0.95
        
        if any(w in analysis.keywords for w in ["详细", "深入", "详"]):
            if "completeness" in alignment:
                alignment["completeness"] = min(alignment["completeness"] + 0.05, 1.0)
        
        return alignment
    
    @staticmethod
    def _format_rules(rules: list) -> str:
        """格式化规则显示"""
        output = []
        for rule in rules:
            emoji = "✓"
            name = rule.replace("_", " ").title()
            output.append(f"  {emoji} {name}")
        return "\n".join(output)
    
    @staticmethod
    def _format_memory(memory: Dict) -> str:
        """格式化记忆配置显示"""
        output = []
        for key, value in memory.items():
            if key != "enabled":
                if isinstance(value, bool):
                    output.append(f"  • {key}: {'✓ 启用' if value else '✗ 禁用'}")
                else:
                    output.append(f"  • {key}: {value}")
        return "\n".join(output) if output else "  (使用默认配置)"
    
    @staticmethod
    def _format_alignment(alignment: Dict[str, float]) -> str:
        """格式化对齐参数显示"""
        output = []
        for key, value in sorted(alignment.items()):
            bar_length = int(value * 20)
            bar = "█" * bar_length + "░" * (20 - bar_length)
            output.append(f"  {key:15} [{bar}] {value:.0%}")
        return "\n".join(output)
    
    def export_plan_markdown(self, plan: AgentDesignPlan, filename: str) -> str:
        """
        导出设计方案为 Markdown 文档
        
        Args:
            plan: 设计方案
            filename: 输出文件名
            
        Returns:
            文件路径
        """
        import os
        
        # 确保输出目录存在
        output_dir = "/workspaces/XIAOJIE/I.QUEUE/mnt/user-data/outputs/agent_plans"
        os.makedirs(output_dir, exist_ok=True)
        
        filepath = os.path.join(output_dir, f"{filename}.md")
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(plan.to_markdown())
        
        print(f"✅ 方案已保存: {filepath}")
        return filepath
    
    def export_plan_yaml(self, plan: AgentDesignPlan, filename: str) -> str:
        """
        导出设计方案为 YAML 配置
        
        Args:
            plan: 设计方案
            filename: 输出文件名
            
        Returns:
            文件路径
        """
        import os
        
        # 确保输出目录存在
        output_dir = "/workspaces/XIAOJIE/I.QUEUE/mnt/user-data/outputs/agent_configs"
        os.makedirs(output_dir, exist_ok=True)
        
        filepath = os.path.join(output_dir, f"{filename}.yaml")
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(plan.to_yaml_config())
        
        print(f"✅ 配置已保存: {filepath}")
        return filepath
    
    def show_approval_interface(self, plan: AgentDesignPlan) -> bool:
        """
        显示用户审核界面
        用户可以：
        1. 查看完整的设计方案
        2. 修改任何配置
        3. 确认执行或取消
        
        Args:
            plan: 设计方案
            
        Returns:
            用户是否确认执行
        """
        print("\n" + "=" * 60)
        print("📋 请审核 Agent 设计方案")
        print("=" * 60)
        print("\n完整方案:\n")
        print(plan.to_markdown())
        print("\n" + "=" * 60)
        print("下一步选项:")
        print("  1. ✅ 确认执行 (一键启动)")
        print("  2. 📝 修改配置")
        print("  3. ❌ 取消")
        print("=" * 60)
        
        # 在实际应用中，这里会呈现交互式界面
        # 现在返回 True 表示"自动确认"（用于演示）
        return True


# 使用示例
if __name__ == "__main__":
    designer = AgentAutoDesigner()
    
    # 示例需求
    requirements = [
        "帮我总结今天的工作内容",
        "为我精选最新的科技和商业新闻",
        "生成我的周报"
    ]
    
    for req in requirements:
        print(f"\n\n{'='*60}")
        print(f"用户需求: {req}")
        print(f"{'='*60}")
        
        # 设计 Agent
        plan = designer.design_agent(req)
        
        # 导出方案
        designer.export_plan_markdown(plan, f"plan_{requirements.index(req)+1}")
