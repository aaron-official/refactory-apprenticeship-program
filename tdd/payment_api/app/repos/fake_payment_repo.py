

class FakePaymentRepo:
    def __init__(self):
        self._customers: dict = {}
        self._payments: dict = {}
        self._refunds: dict = {}

    def clear(self):
        self._customers.clear()
        self._payments.clear()
        self._refunds.clear()

    #  Customers 

    def save_customer(self, customer: dict) -> dict:
        self._customers[customer["id"]] = customer
        return customer

    def find_customer_by_id(self, id: str) -> dict | None:
        return self._customers.get(id)

    def find_customer_by_email(self, email: str) -> dict | None:
        return next(
            (c for c in self._customers.values() if c["email"] == email), None
        )

    #  Payments 

    def save_payment(self, payment: dict) -> dict:
        self._payments[payment["id"]] = payment
        return payment

    def find_payment_by_id(self, id: str) -> dict | None:
        return self._payments.get(id)

    def find_payments_by_customer(self, customer_id: str) -> list[dict]:
        return [p for p in self._payments.values() if p["customerId"] == customer_id]

    #  Refunds 

    def save_refund(self, refund: dict) -> dict:
        self._refunds[refund["id"]] = refund
        return refund

    def find_refund_by_id(self, id: str) -> dict | None:
        return self._refunds.get(id)

    def find_refunds_by_payment(self, payment_id: str) -> list[dict]:
        return [r for r in self._refunds.values() if r["paymentId"] == payment_id]
