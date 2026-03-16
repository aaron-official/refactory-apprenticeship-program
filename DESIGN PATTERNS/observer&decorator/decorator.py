from abc import ABC, abstractmethod

class Bike(ABC):
    @abstractmethod
    def describe(self) -> str:
        pass

    @abstractmethod
    def cost(self) -> int:
        pass


class BasicBike(Bike):
    def describe(self) -> str:
        return "Basic Bike"

    def cost(self) -> int:
        return 500000


class BikeDecorator(Bike):
    def __init__(self, bike: Bike):
        self._bike = bike

    @abstractmethod
    def describe(self) -> str:
        pass

    @abstractmethod
    def cost(self) -> int:
        pass


class RainCover(BikeDecorator):
    def describe(self) -> str:
        return self._bike.describe() + " + Rain Cover"

    def cost(self) -> int:
        return self._bike.cost() + 50000


class DeliveryBag(BikeDecorator):
    def describe(self) -> str:
        return self._bike.describe() + " + Delivery Bag"

    def cost(self) -> int:
        return self._bike.cost() + 80000


class SafetyVest(BikeDecorator):
    def describe(self) -> str:
        return self._bike.describe() + " + Safety Vest"

    def cost(self) -> int:
        return self._bike.cost() + 30000


if __name__ == "__main__":
    bike: Bike = BasicBike()
    print(bike.describe(), "->", f"UGX {bike.cost():,}")

    bike = RainCover(bike)
    print(bike.describe(), "->", f"UGX {bike.cost():,}")

    bike = DeliveryBag(bike)
    print(bike.describe(), "->", f"UGX {bike.cost():,}")

    bike = SafetyVest(bike)
    print(bike.describe(), "->", f"UGX {bike.cost():,}")
