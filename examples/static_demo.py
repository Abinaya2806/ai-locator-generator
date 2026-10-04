"""A small offline demonstration of the scoring layer."""

from ai_locator.models import LocatorCandidate
from ai_locator.scorer import LocatorScorer


candidates = [
    LocatorCandidate(
        locator='page.get_by_role("button", name="Sign in")',
        strategy="role",
        confidence=0.98,
        reason="Semantic role and accessible name.",
        matches=1,
        valid=True,
    ),
    LocatorCandidate(
        locator='page.locator("button.btn-primary")',
        strategy="css",
        confidence=0.80,
        reason="Class-based CSS selector.",
        matches=1,
        valid=True,
    ),
]

for candidate in candidates:
    LocatorScorer().score(candidate)
    print(f"{candidate.score:.0f}: {candidate.locator} -> {candidate.signals}")
