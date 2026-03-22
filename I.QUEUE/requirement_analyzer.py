"""
Requirement Analyzer - Understand user's true needs
Convert natural language requirements into structured analysis results
"""

from typing import Dict, List, Tuple, Any
from dataclasses import dataclass


@dataclass
class RequirementAnalysis:
    """Requirement Analysis Result"""
    requirement: str
    primary_type: str  # "summary", "curation", "report"
    secondary_types: List[str]
    keywords: List[str]
    confidence: float
    memory_needs: Dict[str, Any]
    alignment_hints: Dict[str, float]
    recommendations: List[str]


class RequirementAnalyzer:
    """
    Intelligent Requirement Analyzer
    将用户的自然语言需求转化为 Agent 设计指导
    """
    
    # 需求类型的Keywords匹配
    TYPE_KEYWORDS = {
        "summary": {
            "keywords": ["总结", "汇总", "浓缩", "简化", "摘要", "梳理", "归纳",
                        "summary", "summarize", "compress", "extract", "digest"],
            "skills": ["daily_summarizer"],
            "rules": ["content_safety", "format_consistency"],
            "confidence": 0.95,
            "memory": {
                "retention_days": 7,
                "track_patterns": True,
                "learn_style": True
            },
            "alignment": {
                "clarity": 0.95,
                "conciseness": 0.98,
                "completeness": 0.85
            }
        },
        "curation": {
            "keywords": ["精选", "推荐", "新闻", "筛选", "过滤", "聚合", "收集",
                        "curator", "curate", "filter", "select", "pick", "trending"],
            "skills": ["news_curator"],
            "rules": ["content_safety", "format_consistency"],
            "confidence": 0.92,
            "memory": {
                "retention_days": 30,
                "track_preferences": True,
                "learn_interests": True,
                "cache_sources": True
            },
            "alignment": {
                "relevance": 0.95,
                "timeliness": 0.90,
                "uniqueness": 0.85
            }
        },
        "report": {
            "keywords": ["报告", "日报", "周报", "月报", "汇报", "总结", "统计",
                        "report", "daily", "weekly", "monthly", "generate"],
            "skills": ["report_generator"],
            "rules": ["content_safety", "format_consistency"],
            "confidence": 0.93,
            "memory": {
                "retention_days": 90,
                "track_history": True,
                "learn_format": True,
                "archive_reports": True
            },
            "alignment": {
                "professionalism": 0.98,
                "clarity": 0.95,
                "completeness": 0.90
            }
        }
    }
    
    def analyze(self, requirement: str) -> RequirementAnalysis:
        """
        分析User Requirement
        
        Args:
            requirement: 用户的需求描述
            
        Returns:
            RequirementAnalysis: 详细的分析结果
        """
        requirement_lower = requirement.lower()
        
        # 1. 识别Primary Type
        primary_type, primary_confidence = self._identify_primary_type(requirement_lower)
        
        # 2. 识别次要类型
        secondary_types = self._identify_secondary_types(requirement_lower, primary_type)
        
        # 3. 提取Keywords
        keywords = self._extract_keywords(requirement_lower)
        
        # 4. 获取配置建议
        type_config = self.TYPE_KEYWORDS.get(primary_type, {})
        
        # 5. 推断记忆需求
        memory_needs = self._infer_memory_needs(
            primary_type,
            secondary_types,
            keywords,
            type_config.get("memory", {})
        )
        
        # 6. 设置对齐Priority
        alignment_hints = type_config.get("alignment", {})
        
        # 7. 生成推荐
        recommendations = self._generate_recommendations(
            primary_type,
            secondary_types,
            keywords
        )
        
        return RequirementAnalysis(
            requirement=requirement,
            primary_type=primary_type,
            secondary_types=secondary_types,
            keywords=keywords,
            confidence=primary_confidence,
            memory_needs=memory_needs,
            alignment_hints=alignment_hints,
            recommendations=recommendations
        )
    
    def _identify_primary_type(self, requirement_lower: str) -> Tuple[str, float]:
        """识别主要的需求类型"""
        scores = {}
        
        for req_type, config in self.TYPE_KEYWORDS.items():
            kwds = config.get("keywords", [])
            matches = sum(1 for kwd in kwds if kwd in requirement_lower)
            score = matches / len(kwds) * config.get("confidence", 0.9)
            scores[req_type] = score
        
        # 返回得分最高的类型
        if scores:
            primary_type = max(scores, key=scores.get)
            confidence = scores[primary_type]
        else:
            primary_type = "summary"  # 默认类型
            confidence = 0.5
        
        return primary_type, confidence
    
    def _identify_secondary_types(self, requirement_lower: str, primary_type: str) -> List[str]:
        """识别次要类型"""
        secondary = []
        
        for req_type, config in self.TYPE_KEYWORDS.items():
            if req_type == primary_type:
                continue
            
            kwds = config.get("keywords", [])
            if any(kwd in requirement_lower for kwd in kwds):
                secondary.append(req_type)
        
        return secondary
    
    def _extract_keywords(self, requirement_lower: str) -> List[str]:
        """提取Keywords"""
        # 简单的Keywords提取（可以升级为 NLP）
        all_keywords = []
        
        for config in self.TYPE_KEYWORDS.values():
            all_keywords.extend(config.get("keywords", []))
        
        extracted = [kwd for kwd in all_keywords if kwd in requirement_lower]
        return list(set(extracted))  # 去重
    
    def _infer_memory_needs(self, 
                           primary_type: str,
                           secondary_types: List[str],
                           keywords: List[str],
                           default_memory: Dict) -> Dict[str, Any]:
        """推断Memory Configuration需求"""
        memory = default_memory.copy()
        
        # 根据Keywords调整记忆
        if any(w in keywords for w in ["历史", "历年", "archive", "history"]):
            memory["retention_days"] = 365
            memory["archive"] = True
        
        if any(w in keywords for w in ["学习", "学", "learn", "improve"]):
            memory["learn_from_feedback"] = True
            memory["adaptive"] = True
        
        if any(w in keywords for w in ["items性", "偏好", "preference", "custom"]):
            memory["personalization"] = True
        
        return memory
    
    def _generate_recommendations(self,
                                 primary_type: str,
                                 secondary_types: List[str],
                                 keywords: List[str]) -> List[str]:
        """生成使用建议"""
        recommendations = []
        
        if primary_type == "summary":
            recommendations.extend([
                "建议每天固定时间Run，形成工作习惯",
                "可以配合日历使用，按周/月生成汇总",
                "保存摘要历史，方便对比和回顾"
            ])
        elif primary_type == "curation":
            recommendations.extend([
                "配置你感兴趣的话题分类，提高精准度",
                "定期反馈哪些推荐有用，帮助 Agent 学习",
                "设置推荐频率（每天/每周/每月）"
            ])
        elif primary_type == "report":
            recommendations.extend([
                "建议包含量化指标，让报告更专业",
                "设置报告模板，保持风格一致",
                "定期审查报告质量，持续优化"
            ])
        
        return recommendations
    
    def explain_analysis(self, analysis: RequirementAnalysis) -> str:
        """Generate human-readable analysis explanation"""
        output = []
        
        output.append(f"🔍 Requirement Analysis")
        output.append(f"━━━━━━━━━━━━━━━━━━━")
        output.append(f"")
        
        output.append(f"📌 Primary Type: {analysis.primary_type.upper()}")
        output.append(f"   Confidence: {analysis.confidence:.0%}")
        
        if analysis.secondary_types:
            output.append(f"")
            output.append(f"🔄 Secondary Types:")
            for sec_type in analysis.secondary_types:
                output.append(f"   • {sec_type}")
        
        output.append(f"")
        output.append(f"🎯 Identified Keywords:")
        for keyword in analysis.keywords[:5]:
            output.append(f"   • {keyword}")
        
        output.append(f"")
        output.append(f"💡 Recommendations:")
        for rec in analysis.recommendations:
            output.append(f"   • {rec}")
        
        return "\n".join(output)
