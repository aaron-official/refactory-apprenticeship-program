"""
app/services/payment_service.py
Business logic layer. Depends on a repository interface — no direct DB access.
Refactored with STATUS constants, private helpers, and extracted validators.
"""
import logging
from app.utils.validators import validate_amount, validate_currency, validate_email, generate_id

logger = logging.getLogger(__name__)


class STATUS:
    PENDING = "pending"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


class PaymentService:
    def __init__(self, repo):
        self.repo = repo

    # ── Public API ─────────────────────────────────────────────────────────────

    def create_customer(self, name: str, email: str) -> dict:
        self._validate_name(name)
        self._validate_email_field(email)
        self._assert_email_unique(email)

        customer = {
            "id": generate_id("cus"),
            "name": name,
            "email": email,
        }
        return self.repo.save_customer(customer)

    def create_payment(self, customer_id: str, amount, currency: str) -> dict:
        self._assert_customer_exists(customer_id)
        self._validate_payment_amount(amount)
        self._validate_payment_currency(currency)

        payment = {
            "id": generate_id("pay"),
            "customerId": customer_id,
            "amount": amount,
            "currency": currency,
            "status": STATUS.PENDING,
        }
        return self.repo.save_payment(payment)

    def capture(self, payment_id: str) -> dict:
        payment = self._get_payment_or_raise(payment_id)
        self._transition_status(payment, to=STATUS.SUCCEEDED)
        return self.repo.save_payment(payment)

    def fail(self, payment_id: str) -> dict:
        payment = self._get_payment_or_raise(payment_id)
        logger.warning(f"Payment {payment_id} is being marked as failed.")
        self._transition_status(payment, to=STATUS.FAILED)
        return self.repo.save_payment(payment)

    def refund(self, payment_id: str, amount) -> dict:
        payment = self._get_payment_or_raise(payment_id)
        self._assert_refundable(payment, amount)

        refund = {
            "id": generate_id("ref"),
            "paymentId": payment_id,
            "amount": amount,
            "status": STATUS.SUCCEEDED,
        }
        return self.repo.save_refund(refund)

    def get_payment(self, id: str) -> dict | None:
        return self.repo.find_payment_by_id(id)

    def get_customer(self, id: str) -> dict | None:
        return self.repo.find_customer_by_id(id)

    def get_payments_for_customer(self, customer_id: str) -> list[dict]:
        return self.repo.find_payments_by_customer(customer_id)

    # ── Private helpers ────────────────────────────────────────────────────────

    def _validate_name(self, name: str):
        if not name or not name.strip() or len(name) > 100:
            raise ValueError("Name is required")

    def _validate_email_field(self, email: str):
        if not validate_email(email):
            raise ValueError("Invalid email")

    def _assert_email_unique(self, email: str):
        if self.repo.find_customer_by_email(email):
            raise ValueError("Email already exists")

    def _assert_customer_exists(self, customer_id: str):
        if not self.repo.find_customer_by_id(customer_id):
            raise ValueError("Customer not found")

    def _validate_payment_amount(self, amount):
        if not validate_amount(amount):
            raise ValueError("Invalid amount")

    def _validate_payment_currency(self, currency: str):
        if not validate_currency(currency):
            raise ValueError("Invalid currency")

    def _get_payment_or_raise(self, payment_id: str) -> dict:
        payment = self.repo.find_payment_by_id(payment_id)
        if not payment:
            raise ValueError("Payment not found")
        return payment

    def _transition_status(self, payment: dict, to: str):
        if payment["status"] != STATUS.PENDING:
            if to == STATUS.SUCCEEDED:
                raise ValueError("Cannot capture")
            if to == STATUS.FAILED:
                raise ValueError("Cannot fail")
        payment["status"] = to

    def _assert_refundable(self, payment: dict, amount):
        if payment["status"] == STATUS.PENDING:
            raise ValueError("Cannot refund")
        if payment["status"] == STATUS.FAILED:
            raise ValueError("Cannot refund")

        existing_refunds = self.repo.find_refunds_by_payment(payment["id"])
        already_refunded = sum(r["amount"] for r in existing_refunds)
        if already_refunded + amount > payment["amount"]:
            raise ValueError("Refund exceeds payment amount")

    def get_all_payments(self) -> list[dict]:
        return list(self.repo._payments.values()) if hasattr(self.repo, '_payments') else []

    def get_refund(self, id: str) -> dict | None:
        return self.repo.find_refund_by_id(id)
