# ============================================================
# Strategy Pattern
# ============================================================
# The Strategy Pattern defines a family of algorithms,
# encapsulates each one, and makes them interchangeable.
# It lets the algorithm vary independently from clients that use it.
#
# Key Concepts:
#   1. Strategies: Individual implementations of the algorithms (Mobile Money, Card, Cash).
#   2. Context: The class (PaymentContext) that maintains a reference to a Strategy 
#      and delegates execution to it.
# ============================================================

# Define the Strategies

class MobileMoneyPayment:
    def pay(self, amount):
        print(f"Paid {amount} via Mobile Money")

class CardPayment:
    def pay(self, amount):
        print(f"Paid {amount} via Card")

class CashPayment:
    def pay(self, amount):
        print(f"Paid {amount} via Cash")

# Context Class

class PaymentContext:
    def __init__(self, strategy):
        self.strategy = strategy

    def set_strategy(self, strategy):
        self.strategy = strategy

    def execute_payment(self, amount):
        self.strategy.pay(amount)


# Usage

payment = PaymentContext(MobileMoneyPayment())
payment.execute_payment(50000)

payment.set_strategy(CardPayment())
payment.execute_payment(50000)

payment.set_strategy(CashPayment())
payment.execute_payment(50000)
