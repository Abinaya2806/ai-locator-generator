# AI Locator Generator

AI-assisted Playwright locator generation with live browser validation and deterministic scoring.

## Why this project?

Writing selectors manually is easy. Writing **stable** selectors that survive UI changes is harder.
This project combines an LLM with Playwright itself:

1. Inspect the target DOM element.
2. Extract semantic and structural context.
3. Ask an AI model for several locator candidates.
4. Parse only supported Playwright locator expressions.
5. Validate every candidate against the live page.
6. Score candidates using deterministic automation rules.
7. Rank the best unique, stable locator first.

The AI is a candidate generator—not the source of truth. The browser decides whether a locator actually matches.

## Architecture

```text
Target element
     |
     v
DOM / ARIA extractor
     |
     v
LLM candidate generation
     |
     v
Safe locator parser
     |
     v
Live Playwright validation
     |
     v
Deterministic stability scoring
     |
     v
Ranked locator candidates
```

## Requirements

- Python 3.10+
- An OpenAI API key
- Playwright browsers

The official OpenAI Python SDK currently uses the Responses API as its primary interface for model interaction.

## Setup

```bash
git clone <your-repository-url>
cd ai-locator-generator
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
playwright install chromium
cp .env.example .env
```

Put your API key in `.env`:

```text
OPENAI_API_KEY=...
OPENAI_MODEL=gpt-5.5
```

Never commit `.env`.

## CLI

Identify an element with a CSS selector, then let the engine generate better Playwright locators:

```bash
ai-locator \
  --url https://example.com/login \
  --selector 'button[type="submit"]' \
  --headed
```

Machine-readable output:

```bash
ai-locator \
  --url https://example.com/login \
  --selector 'button[type="submit"]' \
  --json
```

## Python API

```python
from playwright.sync_api import sync_playwright
from ai_locator import LocatorEngine

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://example.com")

    target = page.get_by_role("button", name="Sign in")
    result = LocatorEngine(page).generate(target)

    best = result.candidates[0]
    print(best.locator)
    print(best.score)
    print(best.valid)
```

## Scoring model

The deterministic scorer rewards semantic and stable strategies:

| Signal | Effect |
|---|---:|
| Test ID | +30 |
| Role | +28 |
| Label | +27 |
| Placeholder | +20 |
| Text | +18 |
| CSS | +8 |
| XPath | +3 |
| Exactly one match | +25 |
| Multiple matches | -35 |
| No match | -50 |
| Positional selector | -30 |
| Long XPath | -15 |
| Class-dependent selector | -10 |
| High model confidence | +10 |

The score is deliberately transparent so the project is auditable and testable.

## Safety design

The validator does **not** execute model-generated Python. It only understands a small allow-list of Playwright expressions such as:

- `page.get_by_role(...)`
- `page.get_by_label(...)`
- `page.get_by_test_id(...)`
- `page.get_by_placeholder(...)`
- `page.get_by_text(...)`
- `page.locator(...)`

This avoids using `eval()` on LLM output.

## Tests

```bash
pytest -q
```

Lint:

```bash
ruff check .
```

## Example output

```text
Target: <button>Sign in

Candidates:

1. [PASS] page.get_by_role("button", name="Sign in")
   strategy=role score=91 confidence=0.98
   matches=1 reason=Uses the semantic role and accessible name.
   signals=unique match, high model confidence
```

## Roadmap

- [x] DOM/ARIA extraction
- [x] AI candidate generation
- [x] Safe locator parsing
- [x] Live validation
- [x] Deterministic scoring
- [x] CLI
- [x] Unit tests
- [ ] Playwright trace integration
- [ ] Screenshot + vision-assisted locator generation
- [ ] VS Code extension
- [ ] Chrome extension element picker
- [ ] Locator healing when a test fails
- [ ] Locator quality report for an existing automation suite
- [ ] GitHub Actions CI

## Portfolio positioning

This project demonstrates practical AI-assisted test automation rather than simply calling an LLM API. The important engineering boundary is:

**AI proposes. Playwright validates. Deterministic rules rank.**

That separation makes the system easier to test, debug, and trust.
