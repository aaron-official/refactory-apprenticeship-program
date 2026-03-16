# ============================================================
# Observer Pattern
# ============================================================
# The Observer Pattern defines a one-to-many dependency
# between objects. When the subject (one) changes state,
# all its registered observers (many) are notified automatically.
#
# Analogy: MTN Mobile Money account alerts.
# When money enters or leaves the account (the subject),
# all registered contacts — SMS, Email, App — automatically
# receive a notification. They don't keep checking; they just
# get alerted the moment something changes.
#
# Key Concepts:
#   1. Subject: Maintains a list of observers and notifies them.
#   2. Observers: React whenever the subject changes.
# ============================================================


# Subject (the MoMo Account)

class MoMoAccount:
    def __init__(self):
        self._observers = []
        self._balance = 0

    def register(self, observer):
        self._observers.append(observer)

    def notify_all(self, message):
        for observer in self._observers:
            observer.update(message)

    def deposit(self, amount):
        self._balance += amount
        self.notify_all(f"Deposit of UGX {amount:,} received. New balance: UGX {self._balance:,}")

    def withdraw(self, amount):
        self._balance -= amount
        self.notify_all(f"Withdrawal of UGX {amount:,} made. New balance: UGX {self._balance:,}")


# Observers (the alert channels)

class SMSAlert:
    def update(self, message):
        print(f"[SMS]   {message}")

class EmailAlert:
    def update(self, message):
        print(f"[Email] {message}")

class AppNotification:
    def update(self, message):
        print(f"[App]   {message}")


# Usage

account = MoMoAccount()
account.register(SMSAlert())
account.register(EmailAlert())
account.register(AppNotification())

account.deposit(200000)
account.withdraw(50000)
