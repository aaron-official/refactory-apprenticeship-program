Feature: ocs4dev Assistant Configuration and Customization
  As a power user
  I want to adjust model settings and performance levels
  So that I can customize the AI behavior

  Scenario: Switching Model Providers
    Given the settings panel is open
    When the user selects a different brand name from the "Model Provider" block
    Then the system should update the backend provider for subsequent queries

  Scenario: Adjusting Response Intelligence
    Given the user needs a more detailed answer
    When the user toggles the "Tier" setting to the "Smarter" level
    Then the assistant should prioritize depth over speed in its next response
