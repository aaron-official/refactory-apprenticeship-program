Feature: broRacks Security and API Management
  As a developer
  I want to manage API keys and credentials
  So that I can integrate the gateway securely

  Scenario: Generating New API Keys
    Given the user is in the "API Keys" section
    When the user clicks the "Generate" button
    Then a new masked access code should be created and stored in the list

  Scenario: Accessing Secret Credentials
    Given a masked API key exists in the table
    When the user clicks the "Reveal" icon
    Then the full secret code should become visible for the user to copy
