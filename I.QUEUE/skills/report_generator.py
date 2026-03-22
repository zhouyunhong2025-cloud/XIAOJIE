"""
Report Generator Skill
自动生成专业的日报、周报、月报等报告
"""

from typing import List, Dict, Any
from datetime import datetime
from ..skill import Skill


class ReportGeneratorSkill(Skill):
    """
    报告生成技能 - 自动生成专业的日报/周报/月报
    
    使用场景：
    - 自动生成日报
    - 周报总结
    - 月度总结
    - 项目进展报告
    - 工作汇总
    """
    
    name = "report_generator"
    description = "Generate professional daily/weekly/monthly reports from raw data"
    version = "1.0.0"
    
    def __init__(self, 
                 report_type: str = "daily",
                 include_metrics: bool = True,
                 include_next_steps: bool = True):
        """
        初始化报告生成器
        
        Args:
            report_type: 报告类型 ("daily", "weekly", "monthly")
            include_metrics: 是否包含指标
            include_next_steps: 是否包含后续步骤
        """
        super().__init__()
        self.report_type = report_type.lower()
        self.include_metrics = include_metrics
        self.include_next_steps = include_next_steps
        
        if self.report_type not in ["daily", "weekly", "monthly"]:
            self.report_type = "daily"
    
    def execute(self, content: str) -> Dict[str, Any]:
        """
        执行报告生成
        
        Args:
            content: 原始内容（工作日志、任务列表等）
            
        Returns:
            包含格式化报告的数据字典
        """
        # 解析内容
        parsed_data = self._parse_content(content)
        
        # 结构化报告
        report = self._structure_report(parsed_data)
        
        # 格式化输出
        formatted_report = self._format_report(report)
        
        return {
            "status": "success",
            "report_type": self.report_type,
            "report": formatted_report,
            "sections": len(report),
            "timestamp": datetime.now().isoformat(),
            "data": parsed_data
        }
    
    def _parse_content(self, content: str) -> Dict[str, Any]:
        """解析原始内容"""
        lines = content.split('\n')
        
        parsed = {
            "achievements": [],
            "challenges": [],
            "tasks": [],
            "notes": [],
            "metrics": {}
        }
        
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 识别章节
            if line.startswith('✓') or 'achieve' in line.lower():
                current_section = "achievements"
                line = line.lstrip('✓').strip()
            elif line.startswith('✗') or 'challenge' in line.lower():
                current_section = "challenges"
                line = line.lstrip('✗').strip()
            elif line.startswith('→') or 'task' in line.lower():
                current_section = "tasks"
                line = line.lstrip('→').strip()
            elif line.startswith('#'):
                parsed["notes"].append(line)
                continue
            
            if current_section and line and len(line) > 3:
                parsed[current_section].append(line)
        
        return parsed
    
    def _structure_report(self, parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """结构化报告内容"""
        report = {}
        
        # 标题
        report['title'] = f"{self.report_type.capitalize()} Report"
        report['date'] = datetime.now().strftime("%Y-%m-%d")
        
        # 执行摘要
        report['executive_summary'] = self._generate_summary(parsed_data)
        
        # 主要成就
        if parsed_data["achievements"]:
            report['achievements'] = {
                "title": "Key Achievements",
                "items": parsed_data["achievements"][:5],  # 最多5条
                "count": len(parsed_data["achievements"])
            }
        
        # 挑战和改进
        if parsed_data["challenges"]:
            report['challenges'] = {
                "title": "Challenges & Solutions",
                "items": parsed_data["challenges"][:3],  # 最多3条
                "count": len(parsed_data["challenges"])
            }
        
        # 后续步骤
        if self.include_next_steps and parsed_data["tasks"]:
            report['next_steps'] = {
                "title": "Next Steps",
                "items": parsed_data["tasks"][:5],  # 最多5条
                "count": len(parsed_data["tasks"])
            }
        
        # 指标
        if self.include_metrics:
            report['metrics'] = {
                "title": "Key Metrics",
                "total_achievements": len(parsed_data["achievements"]),
                "total_challenges": len(parsed_data["challenges"]),
                "pending_tasks": len(parsed_data["tasks"]),
                "completion_rate": self._calculate_completion_rate(parsed_data)
            }
        
        return report
    
    def _generate_summary(self, data: Dict[str, Any]) -> str:
        """生成执行摘要"""
        achievements = len(data.get("achievements", []))
        challenges = len(data.get("challenges", []))
        
        if achievements >= 5:
            sentiment = "Highly productive"
        elif achievements >= 3:
            sentiment = "Productive"
        else:
            sentiment = "Moderate"
        
        return f"{sentiment} period with {achievements} key achievements and {challenges} challenges addressed."
    
    def _calculate_completion_rate(self, data: Dict[str, Any]) -> str:
        """计算完成率"""
        total = max(len(data.get("achievements", [])) + len(data.get("challenges", [])), 1)
        completed = len(data.get("achievements", []))
        rate = (completed / total * 100) if total > 0 else 0
        return f"{rate:.1f}%"
    
    def _format_report(self, report: Dict[str, Any]) -> str:
        """格式化报告为易读的文本"""
        output = []
        
        # 标题
        output.append(f"{'=' * 50}")
        output.append(f"📋 {report.get('title', 'Report')}")
        output.append(f"📅 {report.get('date', '')}")
        output.append(f"{'=' * 50}")
        output.append("")
        
        # 执行摘要
        output.append("📌 Executive Summary")
        output.append(f"  {report.get('executive_summary', '')}")
        output.append("")
        
        # 成就
        if 'achievements' in report:
            output.append("✅ Key Achievements")
            for item in report['achievements'].get('items', []):
                output.append(f"  • {item}")
            output.append("")
        
        # 挑战
        if 'challenges' in report:
            output.append("⚠️ Challenges & Solutions")
            for item in report['challenges'].get('items', []):
                output.append(f"  • {item}")
            output.append("")
        
        # 后续步骤
        if 'next_steps' in report:
            output.append("→ Next Steps")
            for item in report['next_steps'].get('items', []):
                output.append(f"  • {item}")
            output.append("")
        
        # 指标
        if 'metrics' in report:
            metrics = report['metrics']
            output.append("📊 Key Metrics")
            output.append(f"  • Achievements: {metrics.get('total_achievements', 0)}")
            output.append(f"  • Challenges: {metrics.get('total_challenges', 0)}")
            output.append(f"  • Pending Tasks: {metrics.get('pending_tasks', 0)}")
            output.append(f"  • Completion Rate: {metrics.get('completion_rate', 'N/A')}")
            output.append("")
        
        output.append(f"{'=' * 50}")
        
        return '\n'.join(output)
