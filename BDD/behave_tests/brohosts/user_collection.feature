Feature: broHOSTS User Collection and Access Control
  As a registered user
  I want to manage my watchlist and authenticate securely
  So that I can personalize my streaming experience

  Scenario: Adding Content to Watchlist
    Given the user is logged in and viewing a movie page
    When the user clicks the "Add to Watchlist" button
    Then the button state should change to "Remove" and the title should appear in their collection

  Scenario: Secure User Authentication
    Given the user is an unregistered guest
    When the user completes the "Create Account" overlay form
    Then the sidebar profile icons should unlock and grant access to the Watchlist feature
