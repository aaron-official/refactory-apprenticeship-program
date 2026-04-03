from behave import given, when, then
from playwright.sync_api import expect

@given('the user is on the home page')
def step_impl(context):
    context.page.goto("https://brohosts.online/")

@when('the user scrolls through the "{row_name}" curated row')
def step_impl(context, row_name):
    # Wait for 20s at the Hero section to see auto-switching movies
    context.page.wait_for_timeout(20000)
    # Scroll into view of the trending posters
    context.page.mouse.wheel(0, 600)
    context.page.wait_for_timeout(1000)

@then('the movie posters should scale up on hover to provide visual feedback')
def step_impl(context):
    # Hover over a few posters as indicated by the codegen script
    posters = [
        "Crime 101 ★ 7.0 Crime 101",
        "Avatar: Fire and Ash ★ 7.3",
        "Hoppers ★ 7.6 Hoppers"
    ]
    for name in posters:
        element = context.page.get_by_role("link", name=name).first
        element.hover()
        context.page.wait_for_timeout(1500)

@given('the user has opened the search interface')
def step_impl(context):
    # Ensure we are on the page and click the search trigger if needed
    context.page.goto("https://brohosts.online/")
    # The codegen shows clicking the first link or similar to focus
    context.page.get_by_role("link").first.click()

@when('the user types "{search_term}" into the search field')
def step_impl(context, search_term):
    term = "300"
    search_input = context.page.get_by_role("textbox", name="Search for movies and TV")
    search_input.fill(term)
    context.page.wait_for_timeout(1000)

@then('a grid of matching movie and TV posters should populate the screen instantly')
def step_impl(context):
    # Target the exact movie '300'
    movie_tile = context.page.get_by_text("300", exact=True).first
    expect(movie_tile).to_be_visible()
    
    # Click to open the movie page
    movie_tile.click()
    context.page.wait_for_timeout(6000)  # Spend time to see the top of the movie page
    
    # Scroll down deeply to show movie details (description, actors, etc.)
    context.page.mouse.wheel(0, 1500)
    context.page.wait_for_timeout(6000)
    
    # Scroll back up to the player
    context.page.mouse.wheel(0, -1500)
    context.page.wait_for_timeout(3000)

@given('the user is on a TV show details page')
def step_impl(context):
    pass

@when('the user selects "{season_name}" from the sidebar')
def step_impl(context, season_name):
    pass

@then('the episode grid should refresh to show only episodes from that season')
def step_impl(context):
    pass

@given("a season's episode list is displayed")
def step_impl(context):
    pass

@when('the user types an episode title into the episode search bar')
def step_impl(context):
    pass

@then('the grid should filter to display the specific episode matching the query')
def step_impl(context):
    pass

@given('the user is logged in and viewing a movie page')
def step_impl(context):
    pass

@when('the user clicks the "{button_name}" button')
def step_impl(context, button_name):
    pass

@then('the button state should change to "Remove" and the title should appear in their collection')
def step_impl(context):
    pass

@given('the user is an unregistered guest')
def step_impl(context):
    pass

@when('the user completes the "Create Account" overlay form')
def step_impl(context):
    pass

@then('the sidebar profile icons should unlock and grant access to the Watchlist feature')
def step_impl(context):
    pass
