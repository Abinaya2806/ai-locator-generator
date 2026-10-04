from ai_locator.models import LocatorCandidate
from ai_locator.scorer import LocatorScorer


def test_role_unique_scores_well():
    candidate = LocatorCandidate(
        locator='page.get_by_role("button", name="Sign in")',
        strategy="role",
        confidence=0.98,
        reason="semantic role",
        matches=1,
        valid=True,
    )
    scored = LocatorScorer().score(candidate)
    assert scored.score >= 60
    assert "unique match" in scored.signals


def test_multiple_matches_are_penalized():
    candidate = LocatorCandidate(
        locator='page.get_by_text("Save")',
        strategy="text",
        confidence=0.9,
        reason="text",
        matches=4,
    )
    scored = LocatorScorer().score(candidate)
    assert "multiple matches" in scored.signals
