"""
AgentForge - Skill System
Replace text-based capability descriptions with typed Python functions.
"""
from functools import wraps
from typing import Callable, List, Optional
import inspect


_SKILL_REGISTRY: dict = {}


def skill(
    name: str = None,
    description: str = "",
    tags: List[str] = None,
    priority: int = 1,
    requires: List[str] = None,
):
    """
    Decorator: Define an agent skill as a Python function.

    Instead of writing:
        "The agent can summarize text, translate languages, and answer questions."

    You write:
        @skill(name="summarize", tags=["text"], priority=2)
        def summarize(text: str) -> str:
            ...

    Args:
        name:        Skill identifier (defaults to function name)
        description: What this skill does (defaults to docstring)
        tags:        Category labels for grouping skills
        priority:    Execution priority (higher = preferred, default=1)
        requires:    List of skill names this skill depends on
    """
    def decorator(fn: Callable):
        skill_name = name or fn.__name__
        skill_doc  = description or (inspect.getdoc(fn) or "")

        meta = {
            "name":        skill_name,
            "description": skill_doc,
            "tags":        tags or [],
            "priority":    priority,
            "requires":    requires or [],
            "fn":          fn,
            "signature":   str(inspect.signature(fn)),
        }
        _SKILL_REGISTRY[skill_name] = meta

        @wraps(fn)
        def wrapper(*args, **kwargs):
            return fn(*args, **kwargs)

        wrapper._skill_meta = meta
        return wrapper

    return decorator


def list_skills(tag: str = None) -> List[dict]:
    """Return all registered skills, optionally filtered by tag."""
    skills = list(_SKILL_REGISTRY.values())
    if tag:
        skills = [s for s in skills if tag in s["tags"]]
    return sorted(skills, key=lambda s: -s["priority"])


def get_skill(name: str) -> Optional[dict]:
    return _SKILL_REGISTRY.get(name)
