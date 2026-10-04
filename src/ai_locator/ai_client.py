import json
import os

from openai import OpenAI

from .models import ElementContext, LocatorCandidate
from .prompts import SYSTEM_PROMPT


class AILocatorClient:
    def __init__(self, client: OpenAI | None = None, model: str | None = None):
        self.client = client or OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-5.5")

    def generate_locators(self, context: ElementContext) -> list[LocatorCandidate]:
        payload = json.dumps(context.__dict__, indent=2, ensure_ascii=False)
        response = self.client.responses.create(
            model=self.model,
            instructions=SYSTEM_PROMPT,
            input=f"ELEMENT CONTEXT:\n{payload}",
        )
        raw = response.output_text.strip()
        data = json.loads(raw)
        candidates = data.get("candidates", [])
        return [LocatorCandidate(**item) for item in candidates]
