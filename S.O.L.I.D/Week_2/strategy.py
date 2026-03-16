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

# ── 1. Define the Strategies ───────────────────────────────

class MobileMoneyPayment:
    def pay(self, amount):
        print(f"Paid {amount} via Mobile Money")

class CardPayment:
    def pay(self, amount):
        print(f"Paid {amount} via Card")

class CashPayment:
    def pay(self, amount):
        # Note: Fixed the typo in the original image where CashPayment 
        # printed "via Mobile Money"
        print(f"Paid {amount} via Cash")

# ── 2. The Context Class ────────────────────────────────────

class PaymentContext:
    """
    Context class that uses a strategy. 
    It can be configured with a strategy and even switch it at runtime.
    """
    def __init__(self, strategy):
        self.strategy = strategy

    def set_strategy(self, strategy):
        """Allows switching the payment logic at runtime."""
        self.strategy = strategy

    def execute_payment(self, amount):
        """Delegates the actual payment work to the strategy."""
        self.strategy.pay(amount)


# ── 3. Usage ───────────────────────────────────────────────

# Initialize context with a specific strategy (Mobile Money)
payment = PaymentContext(MobileMoneyPayment())
payment.execute_payment(50000)
# Output: Paid 50000 via Mobile Money

# Switch strategy at runtime to Card
payment.set_strategy(CardPayment())
payment.execute_payment(50000)
# Output: Paid 50000 via Card

# Switch strategy at runtime to Cash
payment.set_strategy(CashPayment())
payment.execute_payment(50000)
# Output: Paid 50000 via Cash
