from dataclasses import dataclass, field
from typing import Any


@dataclass
class ElementContext:
    tag: str
    text: str | None
    role: str | None
    aria_label: str | None
    test_id: str | None
    name: str | None
    placeholder: str | None
    value: str | None
    attributes: dict[str, str]
    parent_html: str | None
    html: str | None


@dataclass
class LocatorCandidate:
    locator: str
    strategy: str
    confidence: float
    reason: str
    score: float = 0.0
    valid: bool = False
    matches: int = 0
    validation_error: str | None = None
    signals: list[str] = field(default_factory=list)


@dataclass
class LocatorResult:
    context: ElementContext
    candidates: list[LocatorCandidate]
