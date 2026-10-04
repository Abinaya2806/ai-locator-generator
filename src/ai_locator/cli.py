import argparse
import json
import sys

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

from .engine import LocatorEngine


def build_parser():
    parser = argparse.ArgumentParser(description="Generate robust Playwright locators with AI.")
    parser.add_argument("--url", required=True, help="Page URL to inspect")
    parser.add_argument("--selector", required=True, help="CSS selector used to identify the target")
    parser.add_argument("--index", type=int, default=0, help="Target index if selector matches multiple elements")
    parser.add_argument("--headed", action="store_true", help="Show the browser")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    return parser


def main():
    load_dotenv()
    args = build_parser().parse_args()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not args.headed)
        page = browser.new_page()
        page.goto(args.url, wait_until="domcontentloaded")

        target = page.locator(args.selector).nth(args.index)
        if target.count() != 1:
            print(f"Target selector must resolve to the requested element: {args.selector}[{args.index}]", file=sys.stderr)
            browser.close()
            return 2

        result = LocatorEngine(page).generate(target)

        if args.json:
            payload = {
                "context": result.context.__dict__,
                "candidates": [candidate.__dict__ for candidate in result.candidates],
            }
            print(json.dumps(payload, indent=2, ensure_ascii=False))
        else:
            print(f"Target: <{result.context.tag}> {result.context.text or ''}".strip())
            print("\nCandidates:\n")
            for number, candidate in enumerate(result.candidates, 1):
                status = "PASS" if candidate.valid else "FAIL"
                print(f"{number}. [{status}] {candidate.locator}")
                print(f"   strategy={candidate.strategy} score={candidate.score:.0f} confidence={candidate.confidence:.2f}")
                print(f"   matches={candidate.matches} reason={candidate.reason}")
                if candidate.signals:
                    print(f"   signals={', '.join(candidate.signals)}")
                if candidate.validation_error:
                    print(f"   error={candidate.validation_error}")
                print()

        browser.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
