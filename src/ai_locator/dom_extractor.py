from playwright.sync_api import Locator

from .models import ElementContext


class DOMExtractor:
    """Extract a compact, AI-friendly representation of a Playwright element."""

    @staticmethod
    def extract(locator: Locator) -> ElementContext:
        data = locator.evaluate(
            """
            element => {
                const attributes = {};
                for (const attr of element.attributes) {
                    attributes[attr.name] = attr.value;
                }
                const parent = element.parentElement;
                return {
                    tag: element.tagName.toLowerCase(),
                    text: element.innerText ? element.innerText.trim().slice(0, 500) : null,
                    role: element.getAttribute("role"),
                    aria_label: element.getAttribute("aria-label"),
                    test_id: element.getAttribute("data-testid") || element.getAttribute("data-test-id"),
                    name: element.getAttribute("name"),
                    placeholder: element.getAttribute("placeholder"),
                    value: element.getAttribute("value"),
                    attributes: attributes,
                    parent_html: parent ? parent.outerHTML.slice(0, 3000) : null,
                    html: element.outerHTML.slice(0, 3000)
                };
            }
            """
        )
        return ElementContext(**data)
