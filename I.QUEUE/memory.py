"""
AgentForge — Memory System
The "vertical rod" — spans all pipeline layers.

Two modes, one module (just like the Tetris piece):
  - Horizontal (flash):  single-session, wiped when agent resets
  - Vertical   (deep):   persists across sessions, written to disk
"""
import json
import os
import time
from dataclasses import dataclass, field
from typing import Any, List, Optional


@dataclass
class MemoryEntry:
    key:       str
    value:     Any
    layer:     str        # "flash" | "session" | "deep"
    timestamp: float = field(default_factory=time.time)
    ttl:       Optional[float] = None   # seconds, None = forever

    def is_expired(self) -> bool:
        if self.ttl is None:
            return False
        return (time.time() - self.timestamp) > self.ttl


class Memory:
    """
    Layered memory with three resolutions:

    Layer        Lifespan            Analogy
    ──────────── ─────────────────── ───────────────────────
    flash        current run only    working memory / RAM
    session      one conversation    short-term memory
    deep         persists to disk    long-term memory / SSD

    Usage:
        mem = Memory(persist_path=".agentforge/memory.json")

        mem.remember("user_name", "Alice", layer="deep")
        mem.remember("current_task", "write report", layer="flash")

        name = mem.recall("user_name")          # "Alice"
        mem.forget("current_task")
        mem.summarize()                          # print all layers
    """

    def __init__(self, persist_path: Optional[str] = None):
        self._flash:   dict = {}   # wiped every run
        self._session: dict = {}   # wiped when .reset_session() called
        self._deep:    dict = {}   # persisted to disk

        self._persist_path = persist_path
        if persist_path:
            self._load_deep()

    # ── Write ────────────────────────────────────────────────────────────────

    def remember(
        self,
        key:   str,
        value: Any,
        layer: str = "session",
        ttl:   Optional[float] = None,
    ) -> None:
        entry = MemoryEntry(key=key, value=value, layer=layer, ttl=ttl)
        store = self._store_for(layer)
        store[key] = entry
        if layer == "deep" and self._persist_path:
            self._save_deep()

    # ── Read ─────────────────────────────────────────────────────────────────

    def recall(self, key: str, default: Any = None) -> Any:
        """Search flash → session → deep in priority order."""
        for store in (self._flash, self._session, self._deep):
            entry = store.get(key)
            if entry and not entry.is_expired():
                return entry.value
        return default

    def recall_layer(self, layer: str) -> dict:
        """Return all non-expired entries in a layer as {key: value}."""
        store = self._store_for(layer)
        return {k: e.value for k, e in store.items() if not e.is_expired()}

    # ── Delete ────────────────────────────────────────────────────────────────

    def forget(self, key: str) -> None:
        for store in (self._flash, self._session, self._deep):
            store.pop(key, None)
        if self._persist_path:
            self._save_deep()

    def reset_flash(self) -> None:
        self._flash.clear()

    def reset_session(self) -> None:
        self._session.clear()
        self._flash.clear()

    # ── Utilities ─────────────────────────────────────────────────────────────

    def summarize(self) -> str:
        lines = ["Memory summary:"]
        for layer in ("flash", "session", "deep"):
            data = self.recall_layer(layer)
            lines.append(f"  [{layer}]  {len(data)} entries")
            for k, v in list(data.items())[:5]:
                short_v = str(v)[:60] + ("…" if len(str(v)) > 60 else "")
                lines.append(f"    • {k}: {short_v}")
        return "\n".join(lines)

    def as_context_string(self, layers: List[str] = None) -> str:
        """Return memory as a text block to inject into LLM context."""
        layers = layers or ["flash", "session", "deep"]
        parts = []
        for layer in layers:
            data = self.recall_layer(layer)
            if data:
                parts.append(f"[{layer} memory]")
                for k, v in data.items():
                    parts.append(f"  {k}: {v}")
        return "\n".join(parts) if parts else ""

    # ── Persistence ───────────────────────────────────────────────────────────

    def _store_for(self, layer: str) -> dict:
        return {"flash": self._flash, "session": self._session, "deep": self._deep}[layer]

    def _save_deep(self) -> None:
        os.makedirs(os.path.dirname(self._persist_path) or ".", exist_ok=True)
        data = {
            k: {"value": e.value, "timestamp": e.timestamp, "ttl": e.ttl}
            for k, e in self._deep.items()
            if not e.is_expired()
        }
        with open(self._persist_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _load_deep(self) -> None:
        if not os.path.exists(self._persist_path):
            return
        with open(self._persist_path, encoding="utf-8") as f:
            data = json.load(f)
        for k, d in data.items():
            entry = MemoryEntry(
                key=k, value=d["value"], layer="deep",
                timestamp=d["timestamp"], ttl=d.get("ttl"),
            )
            if not entry.is_expired():
                self._deep[k] = entry
