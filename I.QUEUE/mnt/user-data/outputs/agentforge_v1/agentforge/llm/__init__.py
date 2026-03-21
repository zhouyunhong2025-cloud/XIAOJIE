from .base import LLMBackend, LLMResponse
from .openai_backend import OpenAIBackend
from .anthropic_backend import AnthropicBackend


def create_backend(provider: str, **kwargs) -> LLMBackend:
    """
    Factory: get a backend by name.

    Usage:
        llm = create_backend("openai", model="gpt-4o-mini")
        llm = create_backend("anthropic", model="claude-haiku-4-5-20251001")
    """
    providers = {
        "openai":    OpenAIBackend,
        "anthropic": AnthropicBackend,
    }
    if provider not in providers:
        raise ValueError(f"Unknown provider '{provider}'. Choose from: {list(providers)}")
    return providers[provider](**kwargs)


__all__ = ["LLMBackend", "LLMResponse", "OpenAIBackend", "AnthropicBackend", "create_backend"]
