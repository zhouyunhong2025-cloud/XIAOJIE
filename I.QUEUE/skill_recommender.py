"""
Skill Recommender - Intelligent selection of local and open-source skills
Based on requirements analysis, recommend optimal skill combinations for Agent
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class SkillSource(Enum):
    """Skill Source"""
    LOCAL = "local"  # Built-in local skills
    GITHUB = "github"  # GitHub open-source projects
    HUGGINGFACE = "huggingface"  # HuggingFace models
    PYPI = "pypi"  # PyPI packages


@dataclass
class SkillRecommendation:
    """Skill Recommendation"""
    name: str
    description: str
    source: SkillSource
    url: Optional[str] = None
    priority: int = 1  # 1-5, 1 is highest priority
    confidence: float = 0.8
    config: Dict[str, Any] = None  # Recommended configuration
    alternatives: List[str] = None  # Alternatives


class SkillRecommender:
    """
    Intelligent Skill Recommender
    Based on requirement analysis results, recommend the most suitable skills
    """
    
    # Local Skill Library
    LOCAL_SKILLS = {
        "daily_summarizer": {
            "name": "Daily Summarizer",
            "description": "Compress long text into 5-10 key points",
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
            "description": "Curate and categorize relevant content, supporting multiple topics",
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
            "description": "Auto-generate professional daily/weekly/monthly reports",
            "tags": ["report", "generate", "statistics"],
            "priority": 1,
            "config": {
                "report_type": "daily",
                "include_metrics": True,
                "include_next_steps": True
            }
        }
    }
    
    # 开源Skill Recommendation库（示例）
    OPENSOURCE_SKILLS = {
        "text_analysis": {
            "name": "Text Analysis Suite",
            "description": "Advanced text analysis and sentiment analysis",
            "source": SkillSource.GITHUB,
            "url": "https://github.com/facebookresearch/fastText",
            "tags": ["analysis", "sentiment", "nlp"],
            "priority": 2,
            "use_cases": ["curation", "summary"]
        },
        "content_enrichment": {
            "name": "Content Enrichment",
            "description": "Enrich content using NER and entity linking",
            "source": SkillSource.GITHUB,
            "url": "https://github.com/explosion/spacy",
            "tags": ["enrichment", "nlp", "entities"],
            "priority": 2,
            "use_cases": ["curation", "report"]
        },
        "advanced_summarization": {
            "name": "Advanced Summarization",
            "description": "Advanced summarization based on Transformers",
            "source": SkillSource.HUGGINGFACE,
            "url": "https://huggingface.co/models?task=summarization",
            "tags": ["summary", "transformer", "ml"],
            "priority": 2,
            "use_cases": ["summary"]
        },
        "semantic_search": {
            "name": "Semantic Search",
            "description": "Semantic search and content retrieval",
            "source": SkillSource.GITHUB,
            "url": "https://github.com/facebookresearch/faiss",
            "tags": ["search", "retrieval", "semantic"],
            "priority": 3,
            "use_cases": ["curation", "summary"]
        },
        "data_visualization": {
            "name": "Data Visualization",
            "description": "Auto-generate data visualization charts",
            "source": SkillSource.PYPI,
            "url": "https://pypi.org/project/plotly/",
            "tags": ["visualization", "charts", "data"],
            "priority": 2,
            "use_cases": ["report"]
        },
        "web_scraping": {
            "name": "Web Scraping",
            "description": "Efficient web scraping",
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
        Recommend skills based on requirements
        
        Args:
            requirement_type: Primary requirement type
            secondary_types: List of secondary types
            keywords: Extracted keywords
            include_opensource: Whether to include open-source recommendations
            
        Returns:
            List of recommended skills
        """
        recommendations = []
        
        # 1. 添加必要的Local Skills
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
        
        # 2. 添加辅助Local Skills（如果有次要类型）
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
        
        # 3. 添加Open-source Recommendations
        if include_opensource:
            opensource_recs = self._recommend_opensource_skills(
                requirement_type,
                secondary_types,
                keywords
            )
            recommendations.extend(opensource_recs)
        
        # 4. 按Priority和Confidence度排序
        recommendations.sort(key=lambda x: (x.priority, -x.confidence))
        
        return recommendations
    
    def _get_required_local_skills(self, requirement_type: str) -> List[str]:
        """Get required local skills for certain requirement types"""
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
        """Recommend open-source skills"""
        recommendations = []
        
        # 根据需求类型组合次要类型
        all_types = [requirement_type] + secondary_types
        
        # 查找匹配的开源技能
        for skill_name, skill_info in self.OPENSOURCE_SKILLS.items():
            use_cases = skill_info.get("use_cases", [])
            tags = skill_info.get("tags", [])
            
            # Review是否适用
            match_score = 0
            for req_type in all_types:
                if req_type in use_cases:
                    match_score += 1
            
            # ReviewKeywords匹配
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
        Customize skill configuration
        
        Args:
            skill_rec: Original recommendation
            custom_config: Custom configuration
            
        Returns:
            Updated recommendation
        """
        if skill_rec.config is None:
            skill_rec.config = {}
        
        skill_rec.config.update(custom_config)
        return skill_rec
    
    def format_recommendations(self, recommendations: List[SkillRecommendation]) -> str:
        """Format recommendation as human-readable"""
        output = []
        
        output.append("✨ Recommended Skills")
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
            output.append(f"   Source: {rec.source.value} | Priority: P{rec.priority} | Confidence: {rec.confidence:.0%}")
            
            if rec.url:
                output.append(f"   🔗 {rec.url}")
            
            if rec.config:
                output.append(f"   ⚙️ Recommended Config:")
                for key, value in rec.config.items():
                    output.append(f"      • {key}: {value}")
            
            output.append("")
        
        return "\n".join(output)
