"""
内容安全规则
防止生成不安全、不当或有害的内容
"""

from ..rule import Rule


class ContentSafetyRule(Rule):
    """
    内容安全规则
    确保所有输出符合安全和伦理标准
    """
    
    name = "content_safety"
    description = "Ensure all output adheres to safety and ethical standards"
    version = "1.0.0"
    
    # 禁止的关键词列表
    FORBIDDEN_KEYWORDS = [
        '暴力', '仇恨', '歧视', '骚扰'
    ]
    
    def validate(self, content: str) -> bool:
        """
        验证内容是否满足安全标准
        
        Args:
            content: 要验证的内容
            
        Returns:
            True 如果内容安全，False 如果不安全
        """
        # 检查禁止关键词
        content_lower = content.lower()
        for keyword in self.FORBIDDEN_KEYWORDS:
            if keyword.lower() in content_lower:
                return False
        
        return True
    
    def apply(self, content: str) -> str:
        """
        应用规则到内容
        
        Args:
            content: 要处理的内容
            
        Returns:
            处理后的安全内容
        """
        if not self.validate(content):
            return "[Content blocked by safety rule]"
        
        return content
