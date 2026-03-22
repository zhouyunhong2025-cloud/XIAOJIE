"""
News Curator Skill
策展和过滤内容，提取最相关的信息
"""

from typing import List, Dict, Any
from ..skill import Skill


class NewsCuratorSkill(Skill):
    """
    内容策展技能 - 从多个来源精选最有价值的内容
    
    使用场景：
    - 每日新闻精选
    - 技术话题汇总
    - 行业资讯筛选
    - 学术论文推荐
    """
    
    name = "news_curator"
    description = "Curate and filter content to extract the most relevant and valuable information"
    version = "1.0.0"
    
    def __init__(self, 
                 categories: List[str] = None,
                 relevance_threshold: float = 0.7,
                 max_items: int = 10):
        """
        初始化内容策展器
        
        Args:
            categories: 内容分类列表（如 ["tech", "business", "science"]）
            relevance_threshold: 相关性阈值（0-1）
            max_items: 最多返回的条目数
        """
        super().__init__()
        self.categories = categories or ["general"]
        self.relevance_threshold = relevance_threshold
        self.max_items = max_items
    
    def execute(self, content: str) -> Dict[str, Any]:
        """
        执行内容策展
        
        Args:
            content: 原始内容（可以是新闻列表、文章集合等）
            
        Returns:
            包含策展结果的数据字典
        """
        # 提取候选项
        candidates = self._extract_items(content)
        
        # 评分和排序
        scored_items = self._score_items(candidates)
        
        # 过滤和分类
        curated_items = self._filter_and_categorize(scored_items)
        
        return {
            "status": "success",
            "items": curated_items,
            "count": len(curated_items),
            "categories": self.categories,
            "total_candidates": len(candidates),
            "selected_ratio": f"{len(curated_items) / max(len(candidates), 1) * 100:.1f}%"
        }
    
    def _extract_items(self, content: str) -> List[Dict[str, str]]:
        """从内容中提取候选项"""
        # 这里可以解析不同的格式（JSON、CSV、纯文本等）
        items = []
        
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line and len(line) > 10:  # 过滤太短的行
                items.append({
                    "content": line,
                    "source": "parsed",
                    "original": line
                })
        
        return items
    
    def _score_items(self, items: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """为候选项评分"""
        scored = []
        
        for item in items:
            # 计算简单的相关性评分
            content = item.get('content', '').lower()
            
            # 关键词匹配评分
            score = self._calculate_relevance_score(content)
            
            item['relevance_score'] = score
            scored.append(item)
        
        # 按评分排序
        scored.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        
        return scored
    
    def _calculate_relevance_score(self, content: str) -> float:
        """计算内容的相关性评分"""
        score = 0.5  # 基础分
        
        # 关键词评分
        important_keywords = ['新闻', '新的', '突破', '首次', '重要', '优秀', 
                            'news', 'breaking', 'first', 'important', 'excellent']
        
        for keyword in important_keywords:
            if keyword in content:
                score += 0.1
        
        # 长度奖励（太长太短都不好）
        word_count = len(content.split())
        if 20 <= word_count <= 100:
            score += 0.2
        
        return min(score, 1.0)  # 限制最大分值为1.0
    
    def _filter_and_categorize(self, scored_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """过滤和分类项目"""
        # 按阈值过滤
        filtered = [item for item in scored_items 
                   if item.get('relevance_score', 0) >= self.relevance_threshold]
        
        # 限制数量
        filtered = filtered[:self.max_items]
        
        # 添加排名和分类
        for idx, item in enumerate(filtered):
            item['rank'] = idx + 1
            item['category'] = self._classify_item(item.get('content', ''))
        
        return filtered
    
    def _classify_item(self, content: str) -> str:
        """对内容进行分类"""
        content_lower = content.lower()
        
        if any(keyword in content_lower for keyword in ['技术', '代码', 'tech', 'python', 'ai']):
            return "technology"
        elif any(keyword in content_lower for keyword in ['商业', '市场', 'business', 'market']):
            return "business"
        elif any(keyword in content_lower for keyword in ['科学', '研究', 'science', 'research']):
            return "science"
        else:
            return "general"
