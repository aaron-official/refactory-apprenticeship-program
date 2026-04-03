Feature: broHOSTS TV Show Navigation and Episode Management
  As a TV show fan
  I want to navigate seasons and find specific episodes
  So that I can watch exactly what I'm looking for

  Scenario: Selecting a Season
    Given the user is on a TV show details page
    When the user selects "Season 2" from the sidebar
    Then the episode grid should refresh to show only episodes from that season

  Scenario: Searching for a Specific Episode
    Given a season's episode list is displayed
    When the user types an episode title into the episode search bar
    Then the grid should filter to display the specific episode matching the query
