from abc import ABC, abstractmethod
from dataclasses import dataclass


# ==========================================
# 1. INTERFACES (Abstractions)
#    ISP: each interface is small and focused
#    a class only implements what makes sense for it
# ==========================================

class InputDevice(ABC):
    @abstractmethod
    def input_data(self):
        pass

class Processor(ABC):
    @abstractmethod
    def process_data(self, data):
        pass

class Storage(ABC):
    @abstractmethod
    def store_data(self, data):
        pass

    @abstractmethod
    def retrieve_data(self):
        pass

class OutputDevice(ABC):
    @abstractmethod
    def output_data(self, data):
        pass

class Swappable(ABC):
    """
    ISP: Only DesktopComputer implements this.
    Laptop does NOT — because a laptop's keyboard is built-in and cannot be swapped.
    This way Laptop is never forced to implement a method that doesn't apply to it.
    """
    @abstractmethod
    def swap_input_device(self, new_device):
        pass


# ==========================================
# 2. CONCRETE IMPLEMENTATIONS (Low-Level Modules)
#    Each class only implements the interface(s) relevant to it
# ==========================================

class Keyboard(InputDevice):
    """Standard external keyboard — only an InputDevice."""
    def input_data(self):
        print("Receiving input from Keyboard...")
        return "keyboard_raw_data"

    def __str__(self):
        return "Keyboard"


class TouchScreen(InputDevice, OutputDevice):
    """
    ISP DEMO: TouchScreen implements TWO interfaces because it genuinely
    does two jobs — it receives touch input AND displays output.
    It is NOT forced to implement process_data or store_data.
    """
    def input_data(self):
        print("Receiving touch input from TouchScreen...")
        return "touch_raw_data"

    def output_data(self, data):
        print(f"TouchScreen displaying: {data}")

    def __str__(self):
        return "TouchScreen"


class IntelChip(Processor):
    """Intel processor — only a Processor."""
    def process_data(self, data):
        print(f"IntelChip processing: {data}")
        return f"processed_{data}"

    def __str__(self):
        return "IntelChip"


class ARMChip(Processor):
    """ARM processor (used in laptops/mobile) — only a Processor."""
    def process_data(self, data):
        print(f"ARMChip processing: {data}")
        return f"arm_processed_{data}"

    def __str__(self):
        return "ARMChip"


class InternalMemory(Storage):
    """RAM/internal memory — only a Storage device."""
    def __init__(self):
        self._memory = None

    def store_data(self, data):
        print("Storing data to Internal Memory...")
        self._memory = data

    def retrieve_data(self):
        print("Retrieving data from Internal Memory...")
        return self._memory

    def __str__(self):
        return "InternalMemory"


class Monitor(OutputDevice):
    """External monitor — only an OutputDevice."""
    def output_data(self, data):
        print(f"Monitor displaying: {data}")

    def __str__(self):
        return "Monitor"


# ==========================================
# 3. DESCRIPTORS (Reusable Validation)
#    Eliminates boilerplate property/setter code.
#    Each descriptor encapsulates type-checking logic once.
# ==========================================

class ValidatedDevice:
    """A descriptor that ensures an attribute is an instance of a specific type."""
    def __init__(self, expected_type, name):
        self.expected_type = expected_type
        self.name = f"_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.name)

    def __set__(self, obj, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(f"Must be an instance of {self.expected_type.__name__}")
        setattr(obj, self.name, value)


class ValidatedString:
    """A descriptor that ensures an attribute is a non-empty string."""
    def __init__(self, name):
        self.name = f"_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.name)

    def __set__(self, obj, value):
        if not isinstance(value, str):
            raise TypeError(f"{self.name[1:]} must be a string")
        if len(value.strip()) == 0:
            raise ValueError(f"{self.name[1:]} cannot be empty")
        setattr(obj, self.name, value)


# ==========================================
# 4. PARAMETER OBJECTS (Eliminate Long Parameter Lists)
#    Using @dataclass to bundle constructor arguments.
#    Prevents accidental argument swaps since all fields are named.
# ==========================================

@dataclass
class ComputerSpecs:
    """Bundles the 6 constructor args for Computer into one clean object."""
    color: str
    dimensions: str
    input_device: InputDevice
    processor: Processor
    storage: Storage
    output_device: OutputDevice


@dataclass
class LaptopSpecs(ComputerSpecs):
    """Extends ComputerSpecs with laptop-specific fields."""
    built_in_keyboard: InputDevice = None   # type: ignore
    battery_life: int = 0


# ==========================================
# 5. BASE COMPUTER CLASS (High-Level Module)
#    DIP: depends on abstractions, not concrete classes
#    Descriptors handle all validation cleanly at the class level
# ==========================================

class Computer:
    # Descriptors handle all the validation cleanly at the class level!
    color = ValidatedString("color")
    dimensions = ValidatedString("dimensions")
    input_device = ValidatedDevice(InputDevice, "input_device")
    processor = ValidatedDevice(Processor, "processor")
    storage = ValidatedDevice(Storage, "storage")
    output_device = ValidatedDevice(OutputDevice, "output_device")

    def __init__(self, specs: ComputerSpecs):
        # One clean parameter — descriptors still validate each field!
        self.color = specs.color
        self.dimensions = specs.dimensions
        self.input_device = specs.input_device
        self.processor = specs.processor
        self.storage = specs.storage
        self.output_device = specs.output_device

    # ---------- Operations ----------
    def input(self):
        return self.input_device.input_data()

    def process(self, data):
        return self.processor.process_data(data)

    def store(self, data):
        self.storage.store_data(data)

    def retrieve(self):
        return self.storage.retrieve_data()

    def output(self, data):
        self.output_device.output_data(data)

    def __str__(self):
        return (f"Computer(color={self.color}, dimensions={self.dimensions}, "
                f"input={self.input_device}, "
                f"processor={self.processor}, "
                f"storage={self.storage}, "
                f"output={self.output_device})")


# ==========================================
# 6. DESKTOP COMPUTER (Extends Computer)
#    LSP: DesktopComputer fully honours everything Computer promises
#    It ADDS swap_input_device because desktops genuinely support it
# ==========================================

class DesktopComputer(Computer, Swappable):
    """
    LSP DEMO: DesktopComputer can do everything Computer can.
    It also adds swap_input_device() — desktops support external keyboard swaps.
    Anywhere a Computer is expected, a DesktopComputer works perfectly.
    """
    def swap_input_device(self, new_device: InputDevice):
        print(f"Swapping input device to {new_device}...")
        self.input_device = new_device   # goes through the descriptor — validated
        print("Input device swapped successfully.")


# ==========================================
# 7. LAPTOP (Extends Computer)
#    LSP: Laptop fully honours everything Computer promises.
#    It does NOT have swap_input_device — laptops have built-in keyboards.
#    By NOT adding a broken swap method, LSP is never violated.
#
#    ISP: Because swap_input_device lives in its own Swappable interface,
#    Laptop is never forced to implement it — ISP is respected too.
# ==========================================

class Laptop(Computer):
    """
    LSP + ISP DEMO:
    - Laptop does NOT implement swap_input_device.
    - It never promises something it cannot deliver.
    - Anywhere a Computer is expected, a Laptop works perfectly — LSP is safe.
    - Laptop is not forced to have a broken swap method — ISP is respected.

    A Laptop has TWO input devices:
    - built_in_keyboard: always physically attached, cannot be swapped (laptop-specific)
    - input_device: inherited from Computer (e.g. TouchScreen for touch input)
    Both are validated through their own getters and setters.
    """
    # Descriptors for laptop-specific attributes
    built_in_keyboard = ValidatedDevice(InputDevice, "built_in_keyboard")

    def __init__(self, specs: LaptopSpecs):
        super().__init__(specs)  # passes the base ComputerSpecs fields up
        self.built_in_keyboard = specs.built_in_keyboard  # validated by descriptor
        self.battery_life = specs.battery_life

    # ---------- battery_life ----------
    @property
    def battery_life(self):
        return self._battery_life

    @battery_life.setter
    def battery_life(self, value):
        if not isinstance(value, int):
            raise TypeError("battery_life must be an integer (hours)")
        if value <= 0:
            raise ValueError("battery_life must be a positive number")
        self._battery_life = value

    # ---------- LSP FIX ----------
    def input(self):
        """Fulfills the base class contract by returning the laptop's combined input."""
        return self.combined_input()

    def keyboard_input(self):
        """Explicitly use the built-in keyboard for input."""
        return self.built_in_keyboard.input_data()

    def touch_input(self):
        """Explicitly use the touch input device."""
        return self.input_device.input_data()

    def combined_input(self):
        """
        Collect input from BOTH the built-in keyboard and the touchscreen
        at the same time, and return them together as a dictionary.
        This reflects how a real laptop works — both inputs are always available.
        """
        keyboard_data = self.built_in_keyboard.input_data()
        touch_data    = self.input_device.input_data()
        return {
            "keyboard": keyboard_data,
            "touch":    touch_data
        }

    def __str__(self):
        return (f"Laptop(color={self.color}, dimensions={self.dimensions}, "
                f"battery={self._battery_life}hrs, "
                f"built_in_keyboard={self.built_in_keyboard}, "
                f"touch_input={self.input_device}, "
                f"processor={self.processor}, "
                f"storage={self.storage}, "
                f"output={self.output_device})")


# ==========================================
# 8. USAGE
# ==========================================

print("=" * 55)
print("        DESKTOP COMPUTER DEMO")
print("=" * 55)

# Build the parts
desktop_keyboard = Keyboard()
desktop_chip     = IntelChip()
desktop_memory   = InternalMemory()
desktop_monitor  = Monitor()

# Bundle into a specs object — named fields prevent accidental swaps
desktop_specs = ComputerSpecs(
    color="Black",
    dimensions="23-inch",
    input_device=desktop_keyboard,
    processor=desktop_chip,
    storage=desktop_memory,
    output_device=desktop_monitor
)

# Inject specs into DesktopComputer
my_desktop = DesktopComputer(desktop_specs)

print(my_desktop)
print()

# Run the desktop
raw       = my_desktop.input()
processed = my_desktop.process(raw)
my_desktop.store(processed)
retrieved = my_desktop.retrieve()
my_desktop.output(retrieved)

# LSP DEMO: swap the keyboard — desktop supports this
print()
print("--- Swapping keyboard on desktop ---")
my_desktop.swap_input_device(TouchScreen())
raw       = my_desktop.input()       # now using TouchScreen input
my_desktop.output(raw)               # TouchScreen handles output too


print()
print("=" * 55)
print("        LAPTOP DEMO")
print("=" * 55)

# Laptop uses a TouchScreen and ARM chip
laptop_screen = TouchScreen()
laptop_chip   = ARMChip()
laptop_memory = InternalMemory()

laptop_specs = LaptopSpecs(
    color="Silver",
    dimensions="14-inch",
    input_device=laptop_screen,     # touchscreen as the second input
    processor=laptop_chip,
    storage=laptop_memory,
    output_device=laptop_screen,
    built_in_keyboard=Keyboard(),   # fixed built-in keyboard
    battery_life=12
)

my_laptop = Laptop(laptop_specs)

print(my_laptop)
print()

# Both inputs collected at once
print("--- Combined input from Keyboard + TouchScreen ---")
all_inputs = my_laptop.combined_input()

# Process, store, and output each source
for source, data in all_inputs.items():
    print(f"\n  [{source.upper()}]")
    processed = my_laptop.process(data)
    my_laptop.store(processed)
    retrieved = my_laptop.retrieve()
    my_laptop.output(retrieved)

# LSP CHECK: Laptop does NOT have swap_input_device
# It never promised it could — so LSP is never broken
print()
print("--- Laptop has no swap_input_device ---")
print(f"hasattr swap_input_device: {hasattr(my_laptop, 'swap_input_device')}")

print()
print("--- Swappable interface check ---")
print(f"DesktopComputer is Swappable: {isinstance(my_desktop, Swappable)}")  # True
print(f"Laptop is Swappable:          {isinstance(my_laptop, Swappable)}")   # False


print()
print("=" * 55)
print("        GETTER / SETTER VALIDATION DEMO")
print("=" * 55)

# Setter rejects wrong types
print()
print("--- Trying to set color to an integer ---")
try:
    my_desktop.color = 999
except TypeError as e:
    print(f"TypeError caught: {e}")

print()
print("--- Trying to pass a string as input_device ---")
try:
    my_desktop.input_device = "not a device"
except TypeError as e:
    print(f"TypeError caught: {e}")

print()
print("--- Trying to set an empty color ---")
try:
    my_desktop.color = "   "
except ValueError as e:
    print(f"ValueError caught: {e}")

print()
print("--- Valid color change ---")
my_desktop.color = "White"
print(f"Desktop color is now: {my_desktop.color}")


print()
print("=" * 55)
print("        ISP DEMO")
print("=" * 55)

# TouchScreen implements two interfaces — only the relevant ones
ts = TouchScreen()
print(f"TouchScreen is InputDevice:  {isinstance(ts, InputDevice)}")
print(f"TouchScreen is OutputDevice: {isinstance(ts, OutputDevice)}")
print(f"TouchScreen is Processor:    {isinstance(ts, Processor)}")  # False
print(f"TouchScreen is Storage:      {isinstance(ts, Storage)}")    # False