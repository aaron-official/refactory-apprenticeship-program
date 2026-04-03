import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://aaron-official-ocs4dev.hf.space/")
    page.get_by_test_id("textbox").click()
    page.get_by_test_id("textbox").fill("what do i need for a stripe account?")
    page.get_by_role("button", name="Send ➤").click()
    page1 = context.new_page()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
