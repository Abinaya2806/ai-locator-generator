import pytest

from ai_locator.parser import parse_locator


def test_parse_role():
    assert parse_locator('page.get_by_role("button", name="Sign in")') == ("role", ("button", "Sign in"))


def test_parse_test_id():
    assert parse_locator('page.get_by_test_id("login-button")') == ("test_id", ("login-button",))


def test_reject_unsupported_expression():
    with pytest.raises(ValueError):
        parse_locator('__import__("os").system("whoami")')
