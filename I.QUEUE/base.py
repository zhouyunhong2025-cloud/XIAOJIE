"""
AgentForge LLM Backend — Base Interface
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Message:
    role: str    # "system" | "user" | "assistant"
    content: str


@dataclass
class LLMResponse:
    text:         str
    model:        str
    input_tokens: int = 0
    output_tokens: int = 0
    raw:          object = field(default=None, repr=False)


class LLMBackend(ABC):
    """
    Abstract LLM backend.

    Subclass this to add any provider — local models, Gemini, etc.
    Only one method is required: `complete`.
    """

    def __init__(self, model: str = "", temperature: float = 0.7, max_tokens: int = 1024):
        self.model       = model
        self.temperature = temperature
        self.max_tokens  = max_tokens

    @abstractmethod
    def complete(
        self,
        messages: List[Message],
        system:   Optional[str] = None,
    ) -> LLMResponse:
        """Send messages to the LLM and return a response."""
        ...

    def ask(self, prompt: str, system: Optional[str] = None) -> str:
        """Convenience: single user prompt → response text."""
        resp = self.complete([Message("user", prompt)], system=system)
        return resp.text
