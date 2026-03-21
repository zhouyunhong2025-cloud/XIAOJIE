"""
AgentForge — OpenAI Backend
Requires: pip install openai
"""
from typing import List, Optional
from .base import LLMBackend, LLMResponse, Message


class OpenAIBackend(LLMBackend):
    """
    OpenAI backend (GPT-4o, GPT-4o-mini, etc.)

    Usage:
        llm = OpenAIBackend(model="gpt-4o-mini", api_key="sk-...")
        # or set OPENAI_API_KEY env var
    """

    def __init__(
        self,
        model:       str   = "gpt-4o-mini",
        api_key:     str   = None,
        temperature: float = 0.7,
        max_tokens:  int   = 1024,
    ):
        super().__init__(model=model, temperature=temperature, max_tokens=max_tokens)
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("Run: pip install openai")

        import os
        self._client = OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"))

    def complete(self, messages: List[Message], system: Optional[str] = None) -> LLMResponse:
        msgs = []
        if system:
            msgs.append({"role": "system", "content": system})
        msgs += [{"role": m.role, "content": m.content} for m in messages]

        resp = self._client.chat.completions.create(
            model=self.model,
            messages=msgs,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        return LLMResponse(
            text=resp.choices[0].message.content,
            model=resp.model,
            input_tokens=resp.usage.prompt_tokens,
            output_tokens=resp.usage.completion_tokens,
            raw=resp,
        )
