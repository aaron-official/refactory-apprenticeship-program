Feature: ocs4dev Onboarding and Security Entry
  As a user
  I want to use quick suggestions and enter secure passcodes
  So that I can start quickly and keep my data private

  Scenario: Using Quick-Start Suggestions
    Given the main chat input is empty
    When the user clicks a pre-written suggestion pill
    Then the chat box should populate and automatically submit the query

  Scenario: Entering Secure Passcodes
    Given the "Secure Passcode" drawer is expanded
    When the user types a secret key into the protected field
    Then the characters should be masked to ensure privacy during entry
