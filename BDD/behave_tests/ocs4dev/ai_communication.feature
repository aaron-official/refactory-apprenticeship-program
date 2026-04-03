Feature: ocs4dev Interactive AI Communication
  As a developer
  I want to communicate with the AI and view code blocks
  So that I can get technical assistance

  Scenario: Submitting a Technical Query
    Given the user is in the chat interface
    When the user types a question about API integration and clicks "Send"
    Then the assistant's response should stream into a new message bubble

  Scenario: Viewing Code Instructions
    Given the AI has provided an integration guide
    When the user scrolls to the "Instruction Block" within the message
    Then the code should be displayed in a dark-themed, monospaced format for readability
