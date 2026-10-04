from .ai_client import AILocatorClient
from .dom_extractor import DOMExtractor
from .models import LocatorResult
from .scorer import LocatorScorer
from .validator import LocatorValidator


class LocatorEngine:
    def __init__(self, page, ai_client=None):
        self.page = page
        self.ai_client = ai_client or AILocatorClient()
        self.scorer = LocatorScorer()

    def generate(self, target) -> LocatorResult:
        context = DOMExtractor.extract(target)
        candidates = self.ai_client.generate_locators(context)
        validator = LocatorValidator(self.page)

        for candidate in candidates:
            validator.validate(candidate)
            self.scorer.score(candidate)

        candidates.sort(key=lambda item: (item.valid, item.score), reverse=True)
        return LocatorResult(context=context, candidates=candidates)
