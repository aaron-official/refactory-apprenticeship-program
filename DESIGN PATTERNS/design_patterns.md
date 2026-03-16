# Design Patterns

---

## 1. Singleton Pattern (Creational)

Ensures only **one instance** of a class ever exists, with a global access point to it.

```python
class Singleton:
    _instance = None
```
A class variable `_instance` is created and set to `None`. This will later hold the one and only instance. Being a class variable means it is shared across all calls to the class, not reset each time.

```python
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```
`__new__` is the method Python calls when creating a new object, before `__init__` even runs. We override it to intercept the creation process. If no instance exists yet (`_instance is None`), it creates one and stores it. If one already exists, it skips creation and returns the same stored object. This is what enforces the "only one instance" rule.

```python
s1 = Singleton()
s2 = Singleton()
print(s1 is s2)  # True — same instance
```
Even though `Singleton()` is called twice, both `s1` and `s2` point to the exact same object in memory. The `is` keyword checks identity, not just equality — the `True` result confirms they are literally the same object.

**Connecting the code to the pattern:**
The pattern's core rule is "only one instance." The code enforces this through `__new__` — the first time `Singleton()` is called, it creates the instance and stores it in `_instance`. Every call after that skips creation and returns the same stored object. That's why `s1 is s2` is `True` — there is literally only one object, which is exactly what the pattern guarantees.

---

## 2. Strategy Pattern (Behavioral)

Defines a family of interchangeable algorithms and allows the behavior of an object to be **swapped at runtime**.

```python
class MobileMoneyPayment:
    def pay(self, amount):
        print(f"Paid {amount} via Mobile Money")

class CardPayment:
    def pay(self, amount):
        print(f"Paid {amount} via Card")

class CashPayment:
    def pay(self, amount):
        print(f"Paid {amount} via Cash")
```
Each class represents one specific strategy — one way of handling payment. All three share the same method name `pay()` but with different behavior inside. This consistency is important because the context class will call `pay()` on whichever strategy it holds, without knowing which one it is.

```python
class PaymentContext:
    def __init__(self, strategy):
        self.strategy = strategy
```
This is the **context** — the class that needs to perform a payment but doesn't decide how. The strategy is passed in from outside during creation, keeping the context flexible and decoupled from any specific payment method.

```python
    def set_strategy(self, strategy):
        self.strategy = strategy
```
This allows the strategy to be swapped at any point during the program's runtime. You are not locked into one payment method — it can change based on user choice or any other condition.

```python
    def execute_payment(self, amount):
        self.strategy.pay(amount)
```
This delegates the actual work to whichever strategy is currently set. The context itself does not know or care how the payment is processed — it just calls `pay()` and the strategy handles the rest.

```python
payment = PaymentContext(MobileMoneyPayment())
payment.execute_payment(50000)   # Paid 50000 via Mobile Money

payment.set_strategy(CardPayment())
payment.execute_payment(50000)   # Paid 50000 via Card
```
We start with Mobile Money as the strategy. Then we switch to Card using `set_strategy()` and pay again — same context object, completely different behavior. No changes to the context class were needed.

**Connecting the code to the pattern:**
The pattern separates *what needs to be done* from *how it gets done*. `PaymentContext` needs to make a payment but doesn't hardcode the method — the strategy is passed in from outside. When `set_strategy()` is called, the behavior changes instantly without touching the context class at all. This is exactly the pattern: flexible, swappable behavior at runtime.

---

## 3. Observer Pattern (Behavioral)

Defines a **one-to-many** relationship where when one object (subject) changes state, all its dependents (observers) are automatically notified.

```python
class Subject:
    def __init__(self):
        self._observers = []

    def subscribe(self, observer):
        self._observers.append(observer)

    def unsubscribe(self, observer):
        self._observers.remove(observer)

    def notify(self, message):
        for observer in self._observers:
            observer.update(message)

class PhoneObserver:
    def update(self, message):
        print(f"Phone received: {message}")

class EmailObserver:
    def update(self, message):
        print(f"Email received: {message}")

# Usage
subject = Subject()
subject.subscribe(PhoneObserver())
subject.subscribe(EmailObserver())

subject.notify("New order placed!")
# Phone received: New order placed!
# Email received: New order placed!
```

**Connecting the code to the pattern:**
The pattern is about automatic notification. `Subject` maintains a list of observers and calls `update()` on each of them when `notify()` is triggered. Neither the subject nor the observers need to know the details of each other — the subject just broadcasts, and whoever is subscribed reacts. This models the one-to-many relationship the pattern defines.

---

## 4. Decorator Pattern (Structural)

Dynamically **adds responsibilities** to an object without changing its original class or structure.

```python
class BasicRide:
    def cost(self):
        return 5000

    def description(self):
        return "Basic boda ride"

class RainCoverDecorator:
    def __init__(self, ride):
        self._ride = ride

    def cost(self):
        return self._ride.cost() + 1000

    def description(self):
        return self._ride.description() + " + rain cover"

class DeliveryBagDecorator:
    def __init__(self, ride):
        self._ride = ride

    def cost(self):
        return self._ride.cost() + 1500

    def description(self):
        return self._ride.description() + " + delivery bag"

# Usage
ride = BasicRide()
ride = RainCoverDecorator(ride)
ride = DeliveryBagDecorator(ride)

print(ride.description())  # Basic boda ride + rain cover + delivery bag
print(ride.cost())         # 7500
```

**Connecting the code to the pattern:**
The pattern is about layering behavior without modifying the original. `BasicRide` stays untouched — each decorator wraps it and adds its own cost and description on top. You can stack as many decorators as needed and the base object never changes. This is the pattern in action: extending behavior by wrapping, not by editing.

---

## 5. Proxy Pattern (Structural)

Provides a **substitute or placeholder** for another object to control access to it.

```python
class RealDatabase:
    def query(self, sql):
        print(f"Executing query: {sql}")

class DatabaseProxy:
    def __init__(self):
        self._real_db = None

    def query(self, sql):
        if "DROP" in sql.upper():
            print("Access denied: dangerous query blocked.")
            return
        if self._real_db is None:
            self._real_db = RealDatabase()  # only created when needed
        self._real_db.query(sql)

# Usage
proxy = DatabaseProxy()
proxy.query("SELECT * FROM users")   # Executing query: SELECT * FROM users
proxy.query("DROP TABLE users")      # Access denied: dangerous query blocked.
```

**Connecting the code to the pattern:**
The pattern puts a gatekeeper in front of the real object. `DatabaseProxy` has the same `query()` interface as `RealDatabase`, so the client doesn't notice the difference. But behind the scenes, the proxy controls access — blocking dangerous queries and only creating the real database when actually needed. This is exactly the proxy role: same interface, controlled access.

---

## 6. Façade Pattern (Structural)

Provides a **simplified interface** to a complex subsystem, hiding the internal details from the client.

```python
class Engine:
    def start(self):
        print("Engine started")

class FuelSystem:
    def pump_fuel(self):
        print("Fuel pumped")

class ElectricalSystem:
    def power_on(self):
        print("Electrical system on")

class CarFacade:
    def __init__(self):
        self.engine = Engine()
        self.fuel = FuelSystem()
        self.electrical = ElectricalSystem()

    def start_car(self):
        self.electrical.power_on()
        self.fuel.pump_fuel()
        self.engine.start()
        print("Car is ready to drive!")

# Usage
car = CarFacade()
car.start_car()
# Electrical system on
# Fuel pumped
# Engine started
# Car is ready to drive!
```

**Connecting the code to the pattern:**
The pattern hides complexity behind a simple interface. The client doesn't need to know about `Engine`, `FuelSystem`, or `ElectricalSystem` — they just call `start_car()` and everything happens automatically. `CarFacade` coordinates all the subsystems internally. This is the pattern's purpose: one clean entry point to a complex set of operations.

---

## 7. Bridge Pattern (Structural)

**Separates an abstraction from its implementation** so that both can change independently.

```python
# Implementations
class AndroidNotification:
    def send(self, message):
        print(f"Android notification: {message}")

class IOSNotification:
    def send(self, message):
        print(f"iOS notification: {message}")

# Abstraction
class Notification:
    def __init__(self, platform):
        self.platform = platform

    def notify(self, message):
        self.platform.send(message)

class UrgentNotification(Notification):
    def notify(self, message):
        self.platform.send(f"URGENT: {message}")

# Usage
notif = UrgentNotification(AndroidNotification())
notif.notify("Server is down!")   # Android notification: URGENT: Server is down!

notif = UrgentNotification(IOSNotification())
notif.notify("Server is down!")   # iOS notification: URGENT: Server is down!
```

**Connecting the code to the pattern:**
The pattern keeps the *what* and the *how* in separate class hierarchies. `Notification` (and its subclasses) define what kind of notification to send. `AndroidNotification` and `IOSNotification` define how it gets delivered. The two sides are connected through composition — `Notification` holds a reference to a platform. This means you can add new notification types or new platforms without touching the other side, which is exactly what the Bridge pattern enables.
