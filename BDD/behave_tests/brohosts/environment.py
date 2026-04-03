from playwright.sync_api import sync_playwright

def before_all(context):
    context.playwright = sync_playwright().start()
    context.browser = context.playwright.chromium.launch(headless=False, slow_mo=1000)

def after_all(context):
    context.browser.close()
    context.playwright.stop()

def before_scenario(context, scenario):
    context.page = context.browser.new_page()
    # Handle popups: close any page that isn't on the brohosts.online domain
    context.page.on("popup", lambda popup: popup.close() if "brohosts.online" not in popup.url else None)

def after_scenario(context, scenario):
    context.page.close()
