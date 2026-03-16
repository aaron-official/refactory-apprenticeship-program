from abc import ABC, abstractmethod
from typing import List
from dataclasses import dataclass


@dataclass(frozen=True)
class OrderEvent:
    order_id: str
    product:  str
    amount:   float
    location: str


class IObserver(ABC):
    @abstractmethod
    def update(self, event: OrderEvent) -> None:
        pass


class IObservable(ABC):
    @abstractmethod
    def register(self, observer: IObserver) -> None:
        pass

    @abstractmethod
    def unregister(self, observer: IObserver) -> None:
        pass


class INotifier(ABC):
    @abstractmethod
    def notify_all(self, event: OrderEvent) -> None:
        pass


class NotificationManager(IObservable, INotifier):
    def __init__(self):
        self._observers: List[IObserver] = []

    def register(self, observer: IObserver) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def unregister(self, observer: IObserver) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_all(self, event: OrderEvent) -> None:
        for observer in self._observers:
            observer.update(event)


class OrderTracker:
    def __init__(self, notifier: INotifier):
        self._notifier = notifier
        self._orders: List[OrderEvent] = []

    def place_order(self, order_id: str, product: str, amount: float, location: str) -> None:
        event = OrderEvent(order_id=order_id, product=product, amount=amount, location=location)
        self._orders.append(event)
        print(f"\n[ORDER TRACKER] New order → {event}\n")
        self._notifier.notify_all(event)


class FinanceDepartment(IObserver):
    def __init__(self):
        self._total_revenue = 0.0

    def update(self, event: OrderEvent) -> None:
        self._total_revenue += event.amount
        print(f"  [Finance Dashboard]     Order #{event.order_id} | "
              f"Amount: UGX {event.amount:,.0f} | "
              f"Total Revenue: UGX {self._total_revenue:,.0f}")


class ProcurementDepartment(IObserver):
    def __init__(self):
        self._inventory_log: List[str] = []

    def update(self, event: OrderEvent) -> None:
        self._inventory_log.append(event.product)
        units_moved = self._inventory_log.count(event.product)
        print(f"  [Procurement Dashboard] Order #{event.order_id} | "
              f"Product: {event.product} | "
              f"Total units moved: {units_moved}")


class MarketingDepartment(IObserver):
    def __init__(self):
        self._location_counts: dict = {}

    def update(self, event: OrderEvent) -> None:
        self._location_counts[event.location] = self._location_counts.get(event.location, 0) + 1
        top_area = max(self._location_counts, key=self._location_counts.get)
        print(f"  [Marketing Dashboard]   Order #{event.order_id} | "
              f"Area: {event.location} | "
              f"Top performing area: {top_area}")


if __name__ == "__main__":
    notifier = NotificationManager()

    notifier.register(FinanceDepartment())
    notifier.register(ProcurementDepartment())
    notifier.register(MarketingDepartment())

    tracker = OrderTracker(notifier)

    tracker.place_order("ORD-001", product="Rice (50kg)",  amount=120_000, location="Kampala")
    tracker.place_order("ORD-002", product="Maize Flour",  amount=85_000,  location="Gulu")
    tracker.place_order("ORD-003", product="Rice (50kg)",  amount=120_000, location="Kampala")
    tracker.place_order("ORD-004", product="Cooking Oil",  amount=200_000, location="Mbarara")
    tracker.place_order("ORD-005", product="Sugar (2kg)",  amount=45_000,  location="Gulu")