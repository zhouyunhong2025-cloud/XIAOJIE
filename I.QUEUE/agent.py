"""
AgentForge - Agent Class
Assembles skills, rules, pipeline, and alignment into a runnable agent.
"""
from typing import Any, Optional
from .skill     import list_skills, get_skill
from .rule      import evaluate_rules, list_rules, RuleViolation
from .pipeline  import Pipeline, PipelineContext
from .alignment import AlignmentFormula, AlignmentReport


class Agent:
    """
    An agent defined entirely in Python — no text config files needed.

    Traditional setup:
        - system_prompt.txt      (500 lines)
        - skills_description.md  (200 lines)
        - rules.txt              (100 lines)
        - alignment_guide.md     (300 lines)

    AgentForge setup:
        agent = Agent(
            name      = "MyAgent",
            pipeline  = my_pipeline,
            alignment = my_formula,
        )
        result = agent.run("What is 2+2?")
    """

    def __init__(
        self,
        name:        str,
        pipeline:    Pipeline,
        alignment:   Optional[AlignmentFormula] = None,
        description: str = "",
        verbose:     bool = True,
    ):
        self.name        = name
        self.pipeline    = pipeline
        self.alignment   = alignment
        self.description = description
        self.verbose     = verbose

    def run(self, input_data: Any) -> dict:
        if self.verbose:
            print(f"\n🤖 Agent [{self.name}] starting...")
            print(f"   Input: {str(input_data)[:80]}")
            print(f"   Pipeline: {' → '.join(self.pipeline.summary())}\n")

        # 1. Pre-run rule check
        try:
            evaluate_rules(input_data, phase="pre")
        except RuleViolation as e:
            return {"success": False, "error": str(e), "output": None}

        # 2. Execute pipeline
        ctx: PipelineContext = self.pipeline.run(input_data)

        # Get final output (last non-skipped phase)
        final_output = None
        for r in reversed(ctx.results):
            if not r.skipped and r.output is not None:
                final_output = r.output
                break

        # 3. Post-run rule check
        try:
            evaluate_rules(final_output, phase="post")
        except RuleViolation as e:
            return {"success": False, "error": str(e), "output": None}

        # 4. Alignment scoring
        alignment_report: Optional[AlignmentReport] = None
        if self.alignment and final_output is not None:
            alignment_report = self.alignment.evaluate(str(final_output))
            if self.verbose:
                print(f"\n{alignment_report}")

        return {
            "success":   True,
            "output":    final_output,
            "context":   ctx,
            "alignment": alignment_report,
        }

    def describe(self) -> str:
        """Print a full description of this agent's configuration."""
        skills = list_skills()
        rules  = list_rules()
        lines = [
            f"╔══════════════════════════════════════╗",
            f"  Agent: {self.name}",
            f"  {self.description}",
            f"╠══════════════════════════════════════╣",
            f"  📦 Skills ({len(skills)}):",
        ]
        for s in skills:
            lines.append(f"     • {s['name']} [priority={s['priority']}] — {s['description'][:60]}")
        lines.append(f"  📏 Rules ({len(rules)}):")
        for r in rules:
            lines.append(f"     • {r['name']} [{r['severity']}] — {r['description'][:60]}")
        lines.append(f"  🔗 Pipeline:")
        lines.append(f"     {' → '.join(self.pipeline.summary())}")
        if self.alignment:
            lines.append(f"  ⚖️  Alignment:")
            lines.append(f"     {self.alignment.formula_str()}")
        lines.append(f"╚══════════════════════════════════════╝")
        return "\n".join(lines)
