# ============================================================
# Decorator Pattern
# ============================================================
# The Decorator Pattern attaches additional responsibilities
# to an object dynamically. Decorators provide a flexible
# alternative to subclassing for extending functionality.
#
# Analogy: A boda rider starting with a basic bike.
# They add a rain cover, then a delivery bag, then a safety vest.
# The original bike never changed — each addition was just
# wrapped on top of it. You can keep adding or removing extras
# without rebuilding the bike from scratch.
#
# Key Concepts:
#   1. Component: The base object being wrapped (BasicBike).
#   2. Decorators: Wrappers that add behaviour on top of it.
# ============================================================


# Base Component

class BasicBike:
    def describe(self):
        return "Basic Bike"

    def cost(self):
        return 500000


# Decorators

class RainCover(BasicBike):
    def __init__(self, bike):
        self._bike = bike

    def describe(self):
        return self._bike.describe() + " + Rain Cover"

    def cost(self):
        return self._bike.cost() + 50000


class DeliveryBag(BasicBike):
    def __init__(self, bike):
        self._bike = bike

    def describe(self):
        return self._bike.describe() + " + Delivery Bag"

    def cost(self):
        return self._bike.cost() + 80000


class SafetyVest(BasicBike):
    def __init__(self, bike):
        self._bike = bike

    def describe(self):
        return self._bike.describe() + " + Safety Vest"

    def cost(self):
        return self._bike.cost() + 30000


# Usage

bike = BasicBike()
print(bike.describe(), "->", f"UGX {bike.cost():,}")

bike = RainCover(bike)
print(bike.describe(), "->", f"UGX {bike.cost():,}")

bike = DeliveryBag(bike)
print(bike.describe(), "->", f"UGX {bike.cost():,}")

bike = SafetyVest(bike)
print(bike.describe(), "->", f"UGX {bike.cost():,}")
