from .models import LocatorCandidate
from .parser import resolve_locator


class LocatorValidator:
    def __init__(self, page):
        self.page = page

    def validate(self, candidate: LocatorCandidate) -> LocatorCandidate:
        try:
            locator = resolve_locator(self.page, candidate.locator)
            count = locator.count()
            candidate.matches = count
            candidate.valid = count == 1
            if not candidate.valid:
                candidate.validation_error = f"Expected exactly 1 match; found {count}."
        except Exception as exc:
            candidate.valid = False
            candidate.matches = 0
            candidate.validation_error = str(exc)
        return candidate
