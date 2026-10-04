import re

from .models import LocatorCandidate


class LocatorScorer:
    """Deterministic quality score layered on top of the model's confidence."""

    BASE = {
        "test_id": 30,
        "role": 28,
        "label": 27,
        "placeholder": 20,
        "text": 18,
        "css": 8,
        "xpath": 3,
    }

    def score(self, candidate: LocatorCandidate) -> LocatorCandidate:
        score = self.BASE.get(candidate.strategy, 0)
        signals: list[str] = []
        expr = candidate.locator

        if candidate.matches == 1:
            score += 25
            signals.append("unique match")
        elif candidate.matches > 1:
            score -= 35
            signals.append("multiple matches")
        elif candidate.matches == 0:
            score -= 50
            signals.append("no match")

        if re.search(r'\.(first|last|nth)\(', expr):
            score -= 30
            signals.append("positional selector")
        if "//" in expr and expr.count("/") > 4:
            score -= 15
            signals.append("long XPath")
        if re.search(r'class\s*[~^$*|]?=', expr) or "class=" in expr:
            score -= 10
            signals.append("class-dependent selector")
        if re.search(r"id=['\"][0-9a-f]{6,}['\"]", expr, re.I):
            score -= 20
            signals.append("possibly dynamic id")
        if candidate.confidence >= 0.9:
            score += 10
            signals.append("high model confidence")
        elif candidate.confidence < 0.6:
            score -= 5
            signals.append("low model confidence")

        candidate.score = max(0.0, min(100.0, float(score)))
        candidate.signals = signals
        return candidate
