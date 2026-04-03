import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://brohosts.online/")
    with page.expect_popup() as page1_info:
        page.get_by_role("link", name="Avatar: Fire and Ash ★ 7.3").nth(1).click()
    page1 = page1_info.value
    page1.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
