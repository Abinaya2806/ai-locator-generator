from ai_locator.models import LocatorCandidate
from ai_locator.validator import LocatorValidator


class FakeLocator:
    def __init__(self, count):
        self._count = count

    def count(self):
        return self._count


class FakePage:
    def get_by_role(self, role, name=None):
        return FakeLocator(1)


def test_validator_accepts_unique_role():
    candidate = LocatorCandidate(
        locator='page.get_by_role("button", name="Sign in")',
        strategy="role",
        confidence=0.9,
        reason="semantic",
    )
    result = LocatorValidator(FakePage()).validate(candidate)
    assert result.valid is True
    assert result.matches == 1
