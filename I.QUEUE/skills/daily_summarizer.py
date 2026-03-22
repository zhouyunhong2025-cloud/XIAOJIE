"""
Daily Summarizer Skill
将长篇内容浓缩成简洁的要点列表
"""

from typing import List, Dict, Any
from ..skill import Skill


class DailySummarizerSkill(Skill):
    """
    每日总结技能 - 把任何长文本压缩成 5-10 条关键点
    
    使用场景：
    - 每天总结工作内容
    - 浓缩邮件和消息
    - 简化阅读内容
    - 快速笔记整理
    """
    
    name = "daily_summarizer"
    description = "Compress content into 5-10 key bullet points for quick review"
    version = "1.0.0"
    
    def __init__(self, summary_length: int = 7):
        """
        初始化每日总结器
        
        Args:
            summary_length: 摘要中保留的要点数量（默认7条）
        """
        super().__init__()
        self.summary_length = summary_length
    
    def execute(self, content: str) -> Dict[str, Any]:
        """
        执行每日总结
        
        Args:
            content: 要总结的文本内容
            
        Returns:
            包含摘要的数据字典
        """
        # 调用 LLM 进行总结
        prompt = self._build_summarize_prompt(content)
        
        # 通过 LLM backend 执行
        if hasattr(self, 'llm_backend'):
            summary_text = self.llm_backend.call(prompt)
        else:
            # 如果没有 LLM backend，返回简单处理
            summary_text = self._simple_summarize(content)
        
        # 解析摘要为要点列表
        bullet_points = self._parse_bullet_points(summary_text)
        
        return {
            "status": "success",
            "summary": bullet_points,
            "count": len(bullet_points),
            "original_length": len(content.split()),
            "compressed_ratio": f"{len(''.join(bullet_points)) / len(content) * 100:.1f}%"
        }
    
    def _build_summarize_prompt(self, content: str) -> str:
        """构建总结提示词"""
        return f"""你是一个内容精炼专家。请将下面的内容浓缩成 {self.summary_length} 条关键要点。

要求：
1. 用简洁的句子（不超过20字）
2. 保留最重要的信息
3. 按照"✓"开头的格式
4. 内容要点清晰、易于快速浏览

内容：
{content}

请直接输出要点，每行一条："""
    
    def _simple_summarize(self, content: str) -> str:
        """简单的摘要处理（没有 LLM 时使用）"""
        sentences = content.split('。')
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # 取前面的句子作为摘要
        summary_count = min(self.summary_length, len(sentences))
        return '。'.join(sentences[:summary_count]) + '。'
    
    def _parse_bullet_points(self, summary_text: str) -> List[str]:
        """解析摘要文本为要点列表"""
        lines = summary_text.split('\n')
        bullet_points = []
        
        for line in lines:
            line = line.strip()
            if line and len(line) > 3:
                # 移除 "✓", "-", "*" 等前缀符号
                for prefix in ['✓', '-', '*', '•', '◦']:
                    if line.startswith(prefix):
                        line = line[1:].strip()
                        break
                
                bullet_points.append(line)
        
        return bullet_points[:self.summary_length]


class DailySummarySummarizerSkill(DailySummarizerSkill):
    """别名，兼容性类"""
    pass
