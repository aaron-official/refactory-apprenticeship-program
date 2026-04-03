import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://brohosts.online/")
    page.get_by_role("link").first.click()
    page.get_by_role("textbox", name="Search for movies and TV").fill("300")
    with page.expect_popup() as page1_info:
        page.locator("div:nth-child(2) > .relative > .absolute.inset-0 > .w-12").click()
    page1 = page1_info.value
    page1.goto("https://brightadnetwork.com/jump/next.php?r=10112814")
    page1.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
