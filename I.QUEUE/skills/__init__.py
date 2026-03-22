"""
预定义的 I.QUEUE Skills 库
用户可以直接使用这些预制的技能，无需编写代码
"""

from .daily_summarizer import DailySummarizerSkill
from .news_curator import NewsCuratorSkill
from .report_generator import ReportGeneratorSkill

__all__ = [
    'DailySummarizerSkill',
    'NewsCuratorSkill', 
    'ReportGeneratorSkill',
]
