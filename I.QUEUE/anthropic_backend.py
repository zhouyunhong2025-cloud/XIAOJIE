"""
AgentForge — Anthropic Backend
Requires: pip install anthropic
"""
from typing import List, Optional
from .base import LLMBackend, LLMResponse, Message


class AnthropicBackend(LLMBackend):
    """
    Anthropic backend (Claude models)

    Usage:
        llm = AnthropicBackend(model="claude-haiku-4-5-20251001", api_key="sk-ant-...")
        # or set ANTHROPIC_API_KEY env var
    """

    def __init__(
        self,
        model:       str   = "claude-haiku-4-5-20251001",
        api_key:     str   = None,
        temperature: float = 0.7,
        max_tokens:  int   = 1024,
    ):
        super().__init__(model=model, temperature=temperature, max_tokens=max_tokens)
        try:
            import anthropic
        except ImportError:
            raise ImportError("Run: pip install anthropic")

        import os
        self._anthropic = anthropic
        self._client    = anthropic.Anthropic(
            api_key=api_key or os.environ.get("ANTHROPIC_API_KEY")
        )

    def complete(self, messages: List[Message], system: Optional[str] = None) -> LLMResponse:
        msgs = [{"role": m.role, "content": m.content} for m in messages]

        kwargs = dict(
            model=self.model,
            messages=msgs,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        if system:
            kwargs["system"] = system

        resp = self._client.messages.create(**kwargs)
        return LLMResponse(
            text=resp.content[0].text,
            model=resp.model,
            input_tokens=resp.usage.input_tokens,
            output_tokens=resp.usage.output_tokens,
            raw=resp,
        )
