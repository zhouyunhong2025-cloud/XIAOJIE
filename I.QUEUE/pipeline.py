"""
AgentForge - Pipeline System
Replace implicit agent "thinking steps" with explicit, ordered phase functions.
"""
from typing import Callable, List, Any, Optional
from dataclasses import dataclass, field
import time


@dataclass
class PhaseResult:
    phase:    str
    output:   Any
    duration: float
    skipped:  bool = False
    error:    Optional[str] = None


@dataclass
class PipelineContext:
    """Shared state that flows through all phases."""
    input:    Any
    memory:   dict = field(default_factory=dict)
    results:  List[PhaseResult] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

    def get(self, phase: str) -> Optional[Any]:
        """Get the output of a previous phase by name."""
        for r in self.results:
            if r.phase == phase and not r.skipped:
                return r.output
        return None


class Phase:
    """
    One step in an agent's execution pipeline.

    Instead of writing:
        "First understand the user's intent. Then retrieve context.
         Then reason step by step. Finally format the output."

    You write:
        pipeline = Pipeline([
            Phase("intent",   understand_intent,   condition=always),
            Phase("retrieve", retrieve_context,     condition=needs_context),
            Phase("reason",   chain_of_thought,     condition=always),
            Phase("format",   format_output,        condition=always),
        ])
    """
    def __init__(
        self,
        name:      str,
        fn:        Callable[[PipelineContext], Any],
        condition: Callable[[PipelineContext], bool] = None,
        timeout:   float = 30.0,
    ):
        self.name      = name
        self.fn        = fn
        self.condition = condition or (lambda ctx: True)
        self.timeout   = timeout

    def run(self, ctx: PipelineContext) -> PhaseResult:
        if not self.condition(ctx):
            return PhaseResult(phase=self.name, output=None,
                               duration=0.0, skipped=True)
        t0 = time.perf_counter()
        try:
            output = self.fn(ctx)
            return PhaseResult(
                phase=self.name,
                output=output,
                duration=time.perf_counter() - t0,
            )
        except Exception as e:
            return PhaseResult(
                phase=self.name,
                output=None,
                duration=time.perf_counter() - t0,
                error=str(e),
            )


class Pipeline:
    """Ordered sequence of phases that process a PipelineContext."""

    def __init__(self, phases: List[Phase]):
        self.phases = phases

    def run(self, input_data: Any, metadata: dict = None) -> PipelineContext:
        ctx = PipelineContext(input=input_data, metadata=metadata or {})
        for phase in self.phases:
            result = phase.run(ctx)
            ctx.results.append(result)
            if result.error:
                print(f"❌ Phase '{phase.name}' failed: {result.error}")
                break
            status = "⏭️  skip" if result.skipped else f"✅ {result.duration*1000:.1f}ms"
            print(f"  [{status}] {phase.name}")
        return ctx

    def summary(self) -> List[str]:
        return [f"Phase({p.name})" for p in self.phases]
