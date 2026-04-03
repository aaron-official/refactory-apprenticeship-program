Feature: broRacks Payment and Withdrawal Operations
  As a business owner
  I want to collect payments and withdraw funds
  So that I can process transactions efficiently

  Scenario: Initiating a Collection Request
    Given the user is in the "Collect" interface
    When the user submits a customer's phone number and amount
    Then a success box should appear showing the calculated gateway fees

  Scenario: Withdrawing Funds to Mobile Money
    Given the user has sufficient "Available Balance"
    When the user confirms a transfer to a recipient's phone number
    Then a new row with a "Pending" badge should immediately appear in the withdrawal history
