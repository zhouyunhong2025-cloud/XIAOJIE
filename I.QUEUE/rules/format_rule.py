"""
格式一致性规则
确保所有输出保持一致的格式和风格
"""

from ..rule import Rule


class FormatConsistencyRule(Rule):
    """
    格式一致性规则
    确保所有输出保持统一的格式和风格
    """
    
    name = "format_consistency"
    description = "Ensure consistent formatting and style across all outputs"
    version = "1.0.0"
    
    def __init__(self):
        super().__init__()
        self.format_style = "markdown"  # 默认 Markdown 格式
    
    def apply(self, content: str) -> str:
        """
        应用格式规则
        
        Args:
            content: 要格式化的内容
            
        Returns:
            格式化后的内容
        """
        if self.format_style == "markdown":
            return self._apply_markdown_format(content)
        elif self.format_style == "plain":
            return self._apply_plain_format(content)
        else:
            return content
    
    def _apply_markdown_format(self, content: str) -> str:
        """应用 Markdown 格式"""
        lines = content.split('\n')
        formatted_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                formatted_lines.append("")
            elif line.startswith('#'):
                # 已经是标题，保留
                formatted_lines.append(line)
            elif any(line.startswith(prefix) for prefix in ['✓', '-', '*', '•', '◦']):
                # 已经是列表项，保留
                formatted_lines.append(f"- {line}")
            else:
                formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)
    
    def _apply_plain_format(self, content: str) -> str:
        """应用纯文本格式"""
        # 移除所有 Markdown 符号
        content = content.replace('**', '')
        content = content.replace('##', '')
        content = content.replace('`', '')
        return content
