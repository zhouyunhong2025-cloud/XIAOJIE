"""
Skill 推荐器 - 智能选择本地和开源技能
根据需求分析，为 Agent 推荐最优的技能组合
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class SkillSource(Enum):
    """技能来源"""
    LOCAL = "local"  # 本地内置技能
    GITHUB = "github"  # GitHub 开源项目
    HUGGINGFACE = "huggingface"  # HuggingFace 模型
    PYPI = "pypi"  # PyPI 包


@dataclass
class SkillRecommendation:
    """技能推荐"""
    name: str
    description: str
    source: SkillSource
    url: Optional[str] = None
    priority: int = 1  # 1-5，1 最高优先级
    confidence: float = 0.8
    config: Dict[str, Any] = None  # 推荐的配置
    alternatives: List[str] = None  # 替代方案


class SkillRecommender:
    """
    智能技能推荐器
    根据需求分析结果，推荐最适合的技能
    """
    
    # 本地技能库
    LOCAL_SKILLS = {
        "daily_summarizer": {
            "name": "Daily Summarizer",
            "description": "将长文本浓缩成 5-10 个关键要点",
            "tags": ["summary", "compress", "extract"],
            "priority": 1,
            "config": {
                "summary_length": 7,
                "include_metrics": False,
                "auto_save": True
            }
        },
        "news_curator": {
            "name": "News Curator",
            "description": "精选和分类相关内容，支持多个话题",
            "tags": ["curation", "filter", "categorize"],
            "priority": 1,
            "config": {
                "categories": ["technology", "business"],
                "relevance_threshold": 0.7,
                "max_items": 10
            }
        },
        "report_generator": {
            "name": "Report Generator",
            "description": "自动生成专业的日报/周报/月报",
            "tags": ["report", "generate", "statistics"],
            "priority": 1,
            "config": {
                "report_type": "daily",
                "include_metrics": True,
                "include_next_steps": True
            }
        }
    }
    
    # 开源技能推荐库（示例）
    OPENSOURCE_SKILLS = {
        "text_analysis": {
            "name": "Text Analysis Suite",
            "description": "高级文本分析和情感分析",
            "source": SkillSource.GITHUB,
            "url": "https://github.com/facebookresearch/fastText",
            "tags": ["analysis", "sentiment", "nlp"],
            "priority": 2,
            "use_cases": ["curation", "summary"]
        },
        "content_enrichment": {
            "name": "Content Enrichment",
            "description": "使用 NER 和实体链接丰富内容",
            "source": SkillSource.GITHUB,
            "url": "https://github.com/explosion/spacy",
            "tags": ["enrichment", "nlp", "entities"],
            "priority": 2,
            "use_cases": ["curation", "report"]
        },
        "advanced_summarization": {
            "name": "Advanced Summarization",
            "description": "基于 Transformers 的高级摘要生成",
            "source": SkillSource.HUGGINGFACE,
            "url": "https://huggingface.co/models?task=summarization",
            "tags": ["summary", "transformer", "ml"],
            "priority": 2,
            "use_cases": ["summary"]
        },
        "semantic_search": {
            "name": "Semantic Search",
            "description": "语义搜索和内容检索",
            "source": SkillSource.GITHUB,
            "url": "https://github.com/facebookresearch/faiss",
            "tags": ["search", "retrieval", "semantic"],
            "priority": 3,
            "use_cases": ["curation", "summary"]
        },
        "data_visualization": {
            "name": "Data Visualization",
            "description": "自动生成数据可视化图表",
            "source": SkillSource.PYPI,
            "url": "https://pypi.org/project/plotly/",
            "tags": ["visualization", "charts", "data"],
            "priority": 2,
            "use_cases": ["report"]
        },
        "web_scraping": {
            "name": "Web Scraping",
            "description": "高效的网页内容抓取",
            "source": SkillSource.PYPI,
            "url": "https://pypi.org/project/scrapy/",
            "tags": ["scraping", "web", "crawl"],
            "priority": 3,
            "use_cases": ["curation"]
        }
    }
    
    def recommend_skills(self, 
                        requirement_type: str,
                        secondary_types: List[str],
                        keywords: List[str],
                        include_opensource: bool = True) -> List[SkillRecommendation]:
        """
        根据需求推荐技能
        
        Args:
            requirement_type: 主要需求类型
            secondary_types: 次要需求类型列表
            keywords: 提取的关键词
            include_opensource: 是否包含开源推荐
            
        Returns:
            推荐的技能列表
        """
        recommendations = []
        
        # 1. 添加必要的本地技能
        local_skills = self._get_required_local_skills(requirement_type)
        for skill_name in local_skills:
            if skill_name in self.LOCAL_SKILLS:
                skill = self.LOCAL_SKILLS[skill_name]
                rec = SkillRecommendation(
                    name=skill["name"],
                    description=skill["description"],
                    source=SkillSource.LOCAL,
                    priority=1,
                    confidence=0.95,
                    config=skill.get("config")
                )
                recommendations.append(rec)
        
        # 2. 添加辅助本地技能（如果有次要类型）
        for secondary_type in secondary_types:
            auxiliary_skills = self._get_required_local_skills(secondary_type)
            for skill_name in auxiliary_skills:
                if skill_name in self.LOCAL_SKILLS and not any(
                    r.name == self.LOCAL_SKILLS[skill_name]["name"] for r in recommendations
                ):
                    skill = self.LOCAL_SKILLS[skill_name]
                    rec = SkillRecommendation(
                        name=skill["name"],
                        description=skill["description"],
                        source=SkillSource.LOCAL,
                        priority=2,
                        confidence=0.80,
                        config=skill.get("config")
                    )
                    recommendations.append(rec)
        
        # 3. 添加开源推荐
        if include_opensource:
            opensource_recs = self._recommend_opensource_skills(
                requirement_type,
                secondary_types,
                keywords
            )
            recommendations.extend(opensource_recs)
        
        # 4. 按优先级和信心度排序
        recommendations.sort(key=lambda x: (x.priority, -x.confidence))
        
        return recommendations
    
    def _get_required_local_skills(self, requirement_type: str) -> List[str]:
        """获取某个需求类型必需的本地技能"""
        mapping = {
            "summary": ["daily_summarizer"],
            "curation": ["news_curator"],
            "report": ["report_generator"]
        }
        return mapping.get(requirement_type, [])
    
    def _recommend_opensource_skills(self,
                                    requirement_type: str,
                                    secondary_types: List[str],
                                    keywords: List[str]) -> List[SkillRecommendation]:
        """推荐开源技能"""
        recommendations = []
        
        # 根据需求类型组合次要类型
        all_types = [requirement_type] + secondary_types
        
        # 查找匹配的开源技能
        for skill_name, skill_info in self.OPENSOURCE_SKILLS.items():
            use_cases = skill_info.get("use_cases", [])
            tags = skill_info.get("tags", [])
            
            # 检查是否适用
            match_score = 0
            for req_type in all_types:
                if req_type in use_cases:
                    match_score += 1
            
            # 检查关键词匹配
            keyword_matches = sum(1 for kwd in keywords if kwd in tags)
            if keyword_matches > 0:
                match_score += keyword_matches * 0.5
            
            # 如果有匹配，添加推荐
            if match_score > 0:
                rec = SkillRecommendation(
                    name=skill_info["name"],
                    description=skill_info["description"],
                    source=skill_info["source"],
                    url=skill_info.get("url"),
                    priority=skill_info["priority"],
                    confidence=min(0.5 + match_score * 0.1, 0.85)
                )
                recommendations.append(rec)
        
        return recommendations
    
    def customize_config(self,
                        skill_rec: SkillRecommendation,
                        custom_config: Dict[str, Any]) -> SkillRecommendation:
        """
        自定义技能配置
        
        Args:
            skill_rec: 原始推荐
            custom_config: 自定义配置
            
        Returns:
            更新后的推荐
        """
        if skill_rec.config is None:
            skill_rec.config = {}
        
        skill_rec.config.update(custom_config)
        return skill_rec
    
    def format_recommendations(self, recommendations: List[SkillRecommendation]) -> str:
        """格式化推荐为人类可读的形式"""
        output = []
        
        output.append("✨ 推荐的技能")
        output.append("━━━━━━━━━━━━━━━━━━━")
        output.append("")
        
        for idx, rec in enumerate(recommendations, 1):
            emoji = {
                SkillSource.LOCAL: "📦",
                SkillSource.GITHUB: "🐙",
                SkillSource.HUGGINGFACE: "🤗",
                SkillSource.PYPI: "📥"
            }.get(rec.source, "🔧")
            
            output.append(f"{idx}. {emoji} {rec.name}")
            output.append(f"   {rec.description}")
            output.append(f"   来源: {rec.source.value} | 优先级: P{rec.priority} | 信心: {rec.confidence:.0%}")
            
            if rec.url:
                output.append(f"   🔗 {rec.url}")
            
            if rec.config:
                output.append(f"   ⚙️ 建议配置:")
                for key, value in rec.config.items():
                    output.append(f"      • {key}: {value}")
            
            output.append("")
        
        return "\n".join(output)
