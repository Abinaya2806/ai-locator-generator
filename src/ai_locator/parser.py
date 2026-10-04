import re


def parse_locator(expression: str) -> tuple[str, tuple[str, ...]]:
    """Parse the intentionally small, allow-listed locator expression language."""
    expression = expression.strip()

    match = re.fullmatch(
        r'''page\.get_by_role\(\s*['"](.*?)['"](?:\s*,\s*name\s*=\s*['"](.*?)['"])?\s*\)''',
        expression,
    )
    if match:
        role, name = match.groups()
        return "role", (role, name) if name is not None else (role,)

    patterns = {
        "label": r'''page\.get_by_label\(\s*['"](.*?)['"]\s*\)''',
        "test_id": r'''page\.get_by_test_id\(\s*['"](.*?)['"]\s*\)''',
        "placeholder": r'''page\.get_by_placeholder\(\s*['"](.*?)['"]\s*\)''',
        "text": r'''page\.get_by_text\(\s*['"](.*?)['"]\s*\)''',
    }
    for strategy, pattern in patterns.items():
        match = re.fullmatch(pattern, expression)
        if match:
            return strategy, (match.group(1),)

    match = re.fullmatch(r'''page\.locator\(\s*['"](.*?)['"]\s*\)''', expression)
    if match:
        selector = match.group(1)
        strategy = "xpath" if selector.lstrip().startswith(("/", "./", "(")) else "css"
        return strategy, (selector,)

    raise ValueError(f"Unsupported locator expression: {expression}")


def resolve_locator(page, expression: str):
    strategy, values = parse_locator(expression)
    if strategy == "role":
        return page.get_by_role(values[0], name=values[1]) if len(values) == 2 else page.get_by_role(values[0])
    if strategy == "label":
        return page.get_by_label(values[0])
    if strategy == "test_id":
        return page.get_by_test_id(values[0])
    if strategy == "placeholder":
        return page.get_by_placeholder(values[0])
    if strategy == "text":
        return page.get_by_text(values[0])
    if strategy in {"css", "xpath"}:
        return page.locator(values[0])
    raise ValueError(f"Unsupported strategy: {strategy}")
