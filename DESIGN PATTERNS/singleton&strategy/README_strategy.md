# Strategy Design Pattern

## Overview
The **Strategy Design Pattern** allows you to define a family of algorithms (different ways of doing something) and make them **interchangeable**. This lets you switch the "strategy" or "behavior" of an object at runtime without changing the object itself.

## Analogy: Online Checkout Payment
Think of an **Online Store Checkout**. When you're ready to pay, you have different options:
- Pay with **Credit Card**.
- Pay with **PayPal**.
- Pay with **Bitcoin**.

The store (the `PaymentContext`) doesn't care *how* you pay; it just knows it needs to "execute the payment." You can choose your strategy at the last second, and the store just follows the instructions for that specific method.

## How the Code Works
1. **The Strategy Interface (`PaymentStrategy`)**: A rule that says every payment method must have a `pay(amount)` method.
2. **Specific Strategies (`CreditCardPayment`, `PayPalPayment`)**: These are the actual "ways of paying" that follow the rule.
3. **The Context (`PaymentContext`)**: This represents the checkout. It doesn't know the details of how to pay; it just holds onto a `strategy` and calls its `pay()` method when needed.
4. **Interchangeability**: You can start the checkout with a Credit Card, then change your mind and switch it to PayPal. Since both follow the same rules, the checkout keeps working perfectly!

## Code Snippets

### The Context (Swapping Strategies)
```python
class PaymentContext:
    def __init__(self, strategy: PaymentStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: PaymentStrategy):
        # This allows switching the behavior while the program is running
        self._strategy = strategy

    def execute_payment(self, amount: float):
        self._strategy.pay(amount)
```

### The Usage
```python
# Start with Credit Card
context = PaymentContext(CreditCardPayment())
context.execute_payment(100.0)

# Switch to PayPal on the fly
context.set_strategy(PayPalPayment())
context.execute_payment(50.0)
```

## Learning Resources
### Diagrams
- **Online Diagram**: [Strategy Pattern Logic](https://app.diagrams.net/?src=about#G16N82Lm5CBlm4w7gHlV4D0y85aykI-tRz#%7B%22pageId%22%3A%22ZF2uKSElbc-Oh35XiOvH%22%7D)
- **Local PDF Reference**: [singeleton&strategy.pdf](./singeleton&strategy.pdf)

### Presentations
- **Google Slides**: [Singleton & Strategy Presentation](https://docs.google.com/presentation/d/1czLdGu-jWNQqcHLudkvtE30Ok-myi70BnWcnIwEZ4lQ/edit?usp=sharing)
- **Local PPTX**: [Singleton&strategy.pptx](./Singleton&strategy.pptx)
