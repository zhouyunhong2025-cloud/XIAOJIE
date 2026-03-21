"""
AgentForge — AssistantCartridge
================================
The first "墨盒" (ink cartridge / preset).

3 lines to a working agent:

    from agentforge.cartridges import AssistantCartridge
    agent = AssistantCartridge(llm="openai").build()
    result = agent.run("帮我写一份周报")

Resolution levels (分辨率):
    "beginner"  — 4 large blocks, sensible defaults, nothing to configure
    "standard"  — full control over each module via kwargs
    "expert"    — pass your own skill/rule/pipeline functions
"""
from typing import Optional, Callable, List, Any

from ..core.skill     import skill, list_skills
from ..core.rule      import rule, RuleViolation
from ..core.pipeline  import Pipeline, Phase, PipelineContext
from ..core.alignment import (
    AlignmentFormula, AlignmentDimension,
    keyword_avoid_scorer, length_scorer,
)
from ..core.agent     import Agent
from ..memory.memory  import Memory
from ..llm.base       import LLMBackend, Message
from ..llm            import create_backend


# ── Default safety words (overridable) ───────────────────────────────────────
_DEFAULT_BLOCK_WORDS = ["harm", "illegal", "violence", "hate"]


class AssistantCartridge:
    """
    Pre-assembled agent for general assistant use.

    Blocks:
        [SKILL]   understand → think → respond   (横向技能条)
        [MEMORY]  flash + session + deep          (竖棍记忆)
        [RULE]    safety + non-empty              (约束层)
        [ALIGN]   helpfulness × safety × clarity  (对齐公式)

    Args:
        llm:          "openai" | "anthropic" | LLMBackend instance
        model:        model name string (optional, uses sensible default)
        api_key:      API key (or set env var)
        resolution:   "beginner" | "standard" | "expert"
        persona:      system prompt persona string
        block_words:  list of words to block in input
        memory_path:  path to persist deep memory (None = no persistence)
        verbose:      print pipeline trace
    """

    def __init__(
        self,
        llm:          Any           = "openai",
        model:        str           = None,
        api_key:      str           = None,
        resolution:   str           = "beginner",
        persona:      str           = "你是一个专注、简洁、有帮助的助手。",
        block_words:  List[str]     = None,
        memory_path:  Optional[str] = ".agentforge/memory.json",
        verbose:      bool          = True,
    ):
        self.resolution  = resolution
        self.persona     = persona
        self.block_words = block_words or _DEFAULT_BLOCK_WORDS
        self.verbose     = verbose

        # ── LLM backend ──────────────────────────────────────────────────────
        if isinstance(llm, LLMBackend):
            self._llm = llm
        else:
            kwargs = {}
            if model:   kwargs["model"]   = model
            if api_key: kwargs["api_key"] = api_key
            self._llm = create_backend(llm, **kwargs)

        # ── Memory (the vertical rod) ─────────────────────────────────────────
        self._memory = Memory(persist_path=memory_path)

        # ── Conversation history ──────────────────────────────────────────────
        self._history: List[Message] = []

    # ── Build ─────────────────────────────────────────────────────────────────

    def build(self) -> Agent:
        """Assemble and return a ready-to-run Agent."""
        pipeline  = self._build_pipeline()
        alignment = self._build_alignment()
        self._register_rules()

        return Agent(
            name        = f"AssistantAgent [{self.resolution}]",
            description = f"General assistant — resolution={self.resolution}",
            pipeline    = pipeline,
            alignment   = alignment,
            verbose     = self.verbose,
        )

    # ── Internal pipeline construction ───────────────────────────────────────

    def _build_pipeline(self) -> Pipeline:
        llm     = self._llm
        memory  = self._memory
        persona = self.persona
        history = self._history

        def phase_remember(ctx: PipelineContext):
            """Store input in flash memory."""
            memory.remember("last_input", str(ctx.input), layer="flash")
            mem_ctx = memory.as_context_string(["session", "deep"])
            ctx.metadata["memory_context"] = mem_ctx
            return str(ctx.input)

        def phase_think(ctx: PipelineContext):
            """Ask LLM to think step-by-step (beginner: skip; standard+: include)."""
            if self.resolution == "beginner":
                return None   # skip, go straight to respond
            user_input = ctx.get("remember") or str(ctx.input)
            thought = llm.ask(
                f"Think step by step about this request (be brief): {user_input}",
                system="You are a reasoning assistant. Output your thinking in 2-3 steps only."
            )
            memory.remember("last_thought", thought, layer="flash")
            return thought

        def phase_respond(ctx: PipelineContext):
            """Generate the final response."""
            user_input  = ctx.get("remember") or str(ctx.input)
            mem_ctx     = ctx.metadata.get("memory_context", "")
            thought     = ctx.get("think")

            system_parts = [persona]
            if mem_ctx:
                system_parts.append(f"\nContext from memory:\n{mem_ctx}")
            system = "\n".join(system_parts)

            # Build messages with history
            msgs = list(history)
            if thought:
                msgs.append(Message("user",
                    f"My reasoning: {thought}\n\nNow respond to: {user_input}"))
            else:
                msgs.append(Message("user", user_input))

            resp = llm.complete(msgs, system=system)

            # Save to history and memory
            history.append(Message("user", user_input))
            history.append(Message("assistant", resp.text))
            # Keep history bounded
            if len(history) > 20:
                history[:] = history[-20:]

            memory.remember("last_response", resp.text, layer="flash")
            memory.remember(
                f"exchange_{len(history)//2}",
                {"q": user_input[:120], "a": resp.text[:120]},
                layer="session"
            )
            return resp.text

        is_standard_plus = lambda ctx: self.resolution in ("standard", "expert")

        return Pipeline([
            Phase("remember", phase_remember),
            Phase("think",    phase_think,   condition=is_standard_plus),
            Phase("respond",  phase_respond),
        ])

    def _build_alignment(self) -> AlignmentFormula:
        block_words = self.block_words
        return AlignmentFormula(
            dimensions=[
                AlignmentDimension(
                    name="safety",
                    weight=0.40,
                    scorer=keyword_avoid_scorer(block_words),
                    floor=0.80,
                    description="Output avoids blocked content",
                ),
                AlignmentDimension(
                    name="helpfulness",
                    weight=0.40,
                    scorer=lambda text: min(1.0, len(str(text)) / 200),
                    floor=0.40,
                    description="Response is substantive",
                ),
                AlignmentDimension(
                    name="conciseness",
                    weight=0.20,
                    scorer=length_scorer(min_len=10, max_len=2000),
                    floor=0.0,
                    description="Response is within length bounds",
                ),
            ],
            threshold=0.65,
        )

    def _register_rules(self):
        block_words = self.block_words

        @rule(name="assistant_input_safety", severity="block", phase="pre",
              description="Block harmful input")
        def _safety(text: str):
            hits = [w for w in block_words if w in str(text).lower()]
            return len(hits) == 0, f"Blocked words found: {hits}"

        @rule(name="assistant_output_nonempty", severity="error", phase="post",
              description="Response must not be empty")
        def _nonempty(output):
            ok = output is not None and len(str(output).strip()) > 5
            return ok, "Empty or too short response"

    # ── Memory shortcuts (for users who want more) ────────────────────────────

    @property
    def memory(self) -> Memory:
        return self._memory

    def remember(self, key: str, value: Any, layer: str = "deep") -> None:
        """Shortcut: save something to memory directly."""
        self._memory.remember(key, value, layer=layer)

    def recall(self, key: str) -> Any:
        """Shortcut: get from memory."""
        return self._memory.recall(key)
