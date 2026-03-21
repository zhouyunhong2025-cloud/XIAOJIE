"""
AgentForge - Rule Engine
Replace text-based behavioral rules with executable constraint functions.
"""
from functools import wraps
from typing import Callable, List, Any
import inspect


_RULE_REGISTRY: list = []


class RuleViolation(Exception):
    """Raised when an agent action violates a defined rule."""
    def __init__(self, rule_name: str, reason: str, severity: str):
        self.rule_name = rule_name
        self.severity  = severity
        super().__init__(f"[{severity.upper()}] Rule '{rule_name}' violated: {reason}")


def rule(
    name: str = None,
    description: str = "",
    severity: str = "error",   # "warn" | "error" | "block"
    phase: str = "any",        # when to check: "pre" | "post" | "any"
):
    """
    Decorator: Define an agent rule as a constraint function.

    Instead of writing:
        "Never output harmful content. Always cite sources. Keep responses concise."

    You write:
        @rule(name="no_harmful", severity="block")
        def no_harmful_content(output: str) -> tuple[bool, str]:
            flagged = any(w in output for w in HARMFUL_WORDS)
            return (not flagged), "Output contains harmful content"

    The function must return: (passed: bool, reason: str)

    Args:
        name:        Rule identifier
        description: What this rule enforces
        severity:    "warn" (log only) | "error" (raise) | "block" (hard stop)
        phase:       "pre" (before action) | "post" (after action) | "any"
    """
    def decorator(fn: Callable):
        rule_name = name or fn.__name__
        rule_doc  = description or (inspect.getdoc(fn) or "")

        meta = {
            "name":        rule_name,
            "description": rule_doc,
            "severity":    severity,
            "phase":       phase,
            "fn":          fn,
        }
        _RULE_REGISTRY.append(meta)

        @wraps(fn)
        def wrapper(*args, **kwargs):
            return fn(*args, **kwargs)

        wrapper._rule_meta = meta
        return wrapper

    return decorator


def evaluate_rules(context: Any, phase: str = "any") -> List[dict]:
    """
    Run all applicable rules against a context object.

    Returns list of results: [{name, passed, reason, severity}, ...]
    Raises RuleViolation immediately on severity="block" or severity="error".
    """
    results = []
    for r in _RULE_REGISTRY:
        if r["phase"] not in ("any", phase):
            continue
        try:
            passed, reason = r["fn"](context)
        except Exception as e:
            passed, reason = False, f"Rule check error: {e}"

        result = {
            "name":     r["name"],
            "passed":   passed,
            "reason":   reason,
            "severity": r["severity"],
        }
        results.append(result)

        if not passed:
            if r["severity"] in ("error", "block"):
                raise RuleViolation(r["name"], reason, r["severity"])
            elif r["severity"] == "warn":
                print(f"⚠️  WARN [{r['name']}]: {reason}")

    return results


def list_rules() -> List[dict]:
    return [
        {"name": r["name"], "description": r["description"],
         "severity": r["severity"], "phase": r["phase"]}
        for r in _RULE_REGISTRY
    ]
