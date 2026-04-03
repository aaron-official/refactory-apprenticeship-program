import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://brohosts.online/")
    page.get_by_role("link", name="Crime 101 ★ 7.0 Crime 101").first.click()
    page.get_by_role("link", name="Avatar: Fire and Ash ★ 7.3").first.click()
    page.get_by_role("link", name="The Super Mario Galaxy Movie").first.click()
    page.get_by_role("link", name="Hoppers ★ 7.6 Hoppers").first.click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
