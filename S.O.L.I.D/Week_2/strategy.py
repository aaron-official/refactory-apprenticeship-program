# ============================================================
# Strategy Pattern
# ============================================================
# The Strategy Pattern defines a family of algorithms,
# encapsulates each one, and makes them interchangeable.
# It lets the algorithm vary independently from clients that use it.
#
# Key Concepts:
#   1. Strategy: The interface/base class for all algorithms.
#   2. Concrete Strategies: Individual implementations of the algorithms.
#   3. Context: The object that uses a Strategy.
#
# Real-world use cases:
#   - Discount logic in e-commerce (Standard, VIP, Seasonal)
#   - Payment processing (Credit Card, PayPal, Crypto)
#   - Sorting algorithms (QuickSort, MergeSort)
# ============================================================

from abc import ABC, abstractmethod

# ── 1. The Strategy Interface ───────────────────────────────
class PaymentStrategy(ABC):
    """
    Abstract Base Class (ABC) ensuring all strategies implement 
    the pay method.
    """
    @abstractmethod
    def pay(self, amount):
        pass

# ── 2. Concrete Strategies ──────────────────────────────────

class CreditCardPayment(PaymentStrategy):
    def pay(self, amount):
        print(f"Paid ${amount} using Credit Card.")

class PayPalPayment(PaymentStrategy):
    def pay(self, amount):
        print(f"Paid ${amount} using PayPal.")

class CryptoPayment(PaymentStrategy):
    def pay(self, amount):
        print(f"Paid ${amount} using Bitcoin.")

# ── 3. The Context ──────────────────────────────────────────

class ShoppingCart:
    """
    The Context maintains a reference to a Strategy object 
    and delegates the work to it.
    """
    def __init__(self, amount):
        self.amount = amount

    def checkout(self, strategy: PaymentStrategy):
        # The Context doesn't care HOW the payment happens,
        # it just tells the strategy to 'pay'.
        strategy.pay(self.amount)


# ── Usage ───────────────────────────────────────────────────

cart = ShoppingCart(100)

# We can easily swap the algorithm (strategy) at runtime:
cart.checkout(CreditCardPayment()) # Output: Paid $100 using Credit Card.
cart.checkout(PayPalPayment())     # Output: Paid $100 using PayPal.
cart.checkout(CryptoPayment())     # Output: Paid $100 using Bitcoin.
