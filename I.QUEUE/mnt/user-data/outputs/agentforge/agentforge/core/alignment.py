"""
AgentForge - Alignment Formula System
Replace vague alignment text with computable scoring functions.

Traditional: "Be helpful, harmless, and honest."
AgentForge:  alignment_score = weighted_sum([helpfulness, harmlessness, honesty])
"""
from typing import Callable, List, Tuple, Any
from dataclasses import dataclass


@dataclass
class AlignmentDimension:
    """A single measurable alignment axis."""
    name:     str
    weight:   float                          # 0.0 – 1.0
    scorer:   Callable[[Any], float]         # returns score in [0, 1]
    floor:    float = 0.0                    # minimum acceptable score
    description: str = ""


@dataclass
class AlignmentReport:
    overall:    float
    passed:     bool
    dimensions: List[dict]

    def __str__(self):
        lines = [f"Alignment Score: {self.overall:.3f} ({'PASS ✅' if self.passed else 'FAIL ❌'})"]
        for d in self.dimensions:
            bar = "█" * int(d["score"] * 20) + "░" * (20 - int(d["score"] * 20))
            floor_warn = " ⚠️ BELOW FLOOR" if d["score"] < d["floor"] else ""
            lines.append(f"  {d['name']:<18} [{bar}] {d['score']:.3f} (w={d['weight']:.2f}){floor_warn}")
        return "\n".join(lines)


class AlignmentFormula:
    """
    Compute a weighted alignment score from multiple dimensions.

    Instead of writing:
        "Always be helpful. Never be harmful. Strive to be honest.
         Prefer concise answers. Cite your sources."

    You write:
        formula = AlignmentFormula([
            AlignmentDimension("helpfulness",  weight=0.35, scorer=score_helpfulness,  floor=0.5),
            AlignmentDimension("harmlessness", weight=0.35, scorer=score_harmlessness, floor=0.8),
            AlignmentDimension("honesty",      weight=0.20, scorer=score_honesty,       floor=0.6),
            AlignmentDimension("conciseness",  weight=0.10, scorer=score_conciseness,   floor=0.0),
        ])
        report = formula.evaluate(agent_output)
    """

    def __init__(
        self,
        dimensions: List[AlignmentDimension],
        threshold:  float = 0.6,   # minimum overall score to pass
    ):
        total_weight = sum(d.weight for d in dimensions)
        if abs(total_weight - 1.0) > 1e-6:
            # Normalize weights automatically
            for d in dimensions:
                d.weight /= total_weight

        self.dimensions = dimensions
        self.threshold  = threshold

    def evaluate(self, context: Any) -> AlignmentReport:
        """Score a context/output against all dimensions."""
        dim_results = []
        overall     = 0.0
        floor_fail  = False

        for d in self.dimensions:
            try:
                score = float(d.scorer(context))
                score = max(0.0, min(1.0, score))  # clamp
            except Exception as e:
                score = 0.0

            overall += d.weight * score
            if score < d.floor:
                floor_fail = True

            dim_results.append({
                "name":   d.name,
                "score":  score,
                "weight": d.weight,
                "floor":  d.floor,
            })

        passed = (overall >= self.threshold) and (not floor_fail)
        return AlignmentReport(overall=overall, passed=passed, dimensions=dim_results)

    def formula_str(self) -> str:
        """Human-readable formula string."""
        terms = " + ".join(
            f"{d.weight:.2f}×{d.name}" for d in self.dimensions
        )
        return f"score = {terms}  (threshold={self.threshold})"


# ── Utility scorer builders ──────────────────────────────────────────────────

def keyword_avoid_scorer(bad_words: List[str]) -> Callable[[str], float]:
    """Returns 1.0 if no bad words found, else scales down per hit."""
    def scorer(text: str) -> float:
        text_lower = text.lower()
        hits = sum(1 for w in bad_words if w in text_lower)
        return max(0.0, 1.0 - hits * 0.25)
    return scorer


def length_scorer(min_len: int, max_len: int) -> Callable[[str], float]:
    """Score 1.0 if length is within [min_len, max_len]."""
    def scorer(text: str) -> float:
        n = len(text)
        if n < min_len:
            return n / min_len
        if n > max_len:
            return max(0.0, 1.0 - (n - max_len) / max_len)
        return 1.0
    return scorer


def keyword_require_scorer(required: List[str]) -> Callable[[str], float]:
    """Score by fraction of required keywords present."""
    def scorer(text: str) -> float:
        text_lower = text.lower()
        found = sum(1 for w in required if w in text_lower)
        return found / len(required) if required else 1.0
    return scorer
