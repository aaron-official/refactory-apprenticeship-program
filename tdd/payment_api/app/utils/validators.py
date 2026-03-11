"""
app/utils/validators.py
Pure validation helpers — no side effects, no dependencies.
"""
import uuid


def validate_amount(amount) -> bool:
    """Return True only for positive integers (pence/cents). Rejects decimals, strings, None."""
    if not isinstance(amount, int) or isinstance(amount, bool):
        return False
    return amount >= 1


def validate_currency(currency) -> bool:
    """Return True only for exactly 3-character non-empty strings."""
    if not isinstance(currency, str):
        return False
    return len(currency) == 3


def validate_email(email) -> bool:
    """Return True when email contains both '@' and '.'."""
    if not isinstance(email, str) or not email:
        return False
    return "@" in email and "." in email


def generate_id(prefix: str) -> str:
    """Return a prefixed unique string e.g. 'pay_a1b2c3d4'."""
    return f"{prefix}_{uuid.uuid4().hex[:8]}"
