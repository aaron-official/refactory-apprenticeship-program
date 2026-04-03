Feature: broHOSTS Cinematic Discovery and Search
  As a movie enthusiast
  I want to browse and search for content
  So that I can easily discover new titles

  Scenario: Browsing Featured Content
    Given the user is on the home page
    When the user scrolls through the "Trending Now" curated row
    Then the movie posters should scale up on hover to provide visual feedback

  Scenario: Finding a Title via Live Search
    Given the user has opened the search interface
    When the user types "300" into the search field
    Then a grid of matching movie and TV posters should populate the screen instantly
