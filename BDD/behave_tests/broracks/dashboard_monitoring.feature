Feature: broRacks Dashboard and Activity Monitoring
  As a fintech user
  I want to monitor my dashboard and audit transactions
  So that I have a clear overview of my financial status

  Scenario: Monitoring Wallet Balances
    Given the user is logged into the dashboard
    When the dashboard loads the "Command Center"
    Then the "Available Balance" should display in glowing neon green with real-time updates

  Scenario: Auditing Transaction Details
    Given the user is viewing the "Transactions" table
    When the user clicks on a specific transaction row
    Then a side panel should reveal the unique tracking ID and exact timestamp of the movement
