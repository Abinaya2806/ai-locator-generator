from playwright.sync_api import sync_playwright

from ai_locator.engine import LocatorEngine


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.set_content("""
        <main>
          <form aria-label="Login form">
            <label>Email <input type="email" aria-label="Email address"></label>
            <button type="submit">Sign in</button>
          </form>
        </main>
    """)

    target = page.get_by_role("button", name="Sign in")
    result = LocatorEngine(page).generate(target)

    for candidate in result.candidates:
        print(candidate)

    browser.close()
