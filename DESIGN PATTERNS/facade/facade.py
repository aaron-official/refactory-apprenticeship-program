from abc import ABC, abstractmethod
import functools

# ─── Abstract Base for all Subsystems ─────────────────────
class SubSystem(ABC):
    """All subsystems must implement initialize and shutdown."""
    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def shutdown(self):
        pass


# ─── Subsystem Classes ─────────────────────────────────────
class FuelSystem(SubSystem):
    def initialize(self):
        print("  ⛽ Fuel injected into cylinders")
    def inject(self):
        print("  ⛽ Fuel flow increased")
    def cut_fuel(self):
        print("  ⛽ Fuel supply cut")
    def shutdown(self):
        print("  ⛽ Fuel system offline")


class Battery(SubSystem):
    def initialize(self):
        print("  🔋 Battery charge verified — OK")
    def shutdown(self):
        print("  🔋 Battery disconnected")


class AirMixer(SubSystem):
    def initialize(self):
        print("  💨 Air-fuel mixture prepared")
    def increase_airflow(self):
        print("  💨 Airflow increased")
    def shutdown(self):
        print("  💨 Air intake closed")


class Ignition(SubSystem):
    def initialize(self):
        print("  🔥 Spark plugs triggered")
    def shutdown(self):
        print("  🔥 Ignition off")


class Engine(SubSystem):
    def initialize(self):
        print("  🌀 Engine running")
    def rev_up(self):
        print("  🌀 Engine revving up")
    def rev_down(self):
        print("  🌀 Engine cooling down")
    def shutdown(self):
        print("  🌀 Engine stopped")


class BrakeSystem(SubSystem):
    def initialize(self):
        print("  🛑 Brake system ready")
    def apply_brakes(self):
        print("  🛑 Brakes applied")
    def release_brakes(self):
        print("  🛑 Brakes released")
    def shutdown(self):
        print("  🛑 Brake system offline")


class SensorArray(SubSystem):
    def initialize(self):
        print("  💡 All sensors online")
    def shutdown(self):
        print("  💡 Sensors offline")


# ─── Decorator for the running guard ──────────────────────
def requires_running(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self._running:
            print(f"⚠️  Can't {method.__name__.replace('_', ' ')} — car is not started.\n")
            return
        return method(self, *args, **kwargs)
    return wrapper


# ─── The Facade ────────────────────────────────────────────
class Car:
    """
    The Facade.
    The Driver only ever calls these four methods:
    turn_key(), accelerate(), brake(), shut_down()
    Everything else is hidden.
    """
    def __init__(self):
        self._fuel     = FuelSystem()
        self._battery  = Battery()
        self._air      = AirMixer()
        self._ignition = Ignition()
        self._engine   = Engine()
        self._brakes   = BrakeSystem()
        self._sensors  = SensorArray()
        self._running  = False

    def turn_key(self):
        """Start the car — coordinates 7 subsystems."""
        print("🔑 Turning the key...\n")
        self._battery.initialize()
        self._fuel.initialize()
        self._air.initialize()
        self._ignition.initialize()
        self._engine.initialize()
        self._brakes.initialize()
        self._sensors.initialize()
        self._running = True
        print("\n✅ Car started. Ready to drive!\n")

    @requires_running
    def accelerate(self):
        """Press the accelerator — driver has no idea what happens under the hood."""
        print("🚗 Accelerating...\n")
        self._fuel.inject()
        self._air.increase_airflow()
        self._engine.rev_up()
        self._brakes.release_brakes()
        print()

    @requires_running
    def brake(self):
        """Press the brake pedal."""
        print("🛑 Braking...\n")
        self._engine.rev_down()
        self._fuel.cut_fuel()
        self._brakes.apply_brakes()
        print()

    @requires_running
    def shut_down(self):
        """Turn the car off — shuts everything down in safe order."""
        print("🔴 Shutting down...\n")
        self._brakes.apply_brakes()
        self._engine.shutdown()
        self._fuel.shutdown()
        self._air.shutdown()
        self._ignition.shutdown()
        self._sensors.shutdown()
        self._battery.shutdown()
        self._running = False
        print("\n✅ Car safely shut down.\n")


# ─── Client Class ──────────────────────────────────────────
class Driver:
    """
    The Client.
    Only depends on Car (the Facade) —
    knows nothing about any subsystem.
    """
    def __init__(self, car: Car):
        self.car = car

    def hit_the_road(self):
        self.car.turn_key()
        self.car.accelerate()
        self.car.brake()
        self.car.shut_down()


# ─── Run it ────────────────────────────────────────────────
if __name__ == "__main__":
    driver = Driver(Car())
    driver.hit_the_road()