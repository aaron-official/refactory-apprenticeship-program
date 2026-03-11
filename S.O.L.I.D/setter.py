from abc import ABC, abstractmethod


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


class IntelChip(Processor):
    """Intel processor — only a Processor."""
    def process_data(self, data):
        print(f"IntelChip processing: {data}")
        return f"processed_{data}"


class ARMChip(Processor):
    """ARM processor (used in laptops/mobile) — only a Processor."""
    def process_data(self, data):
        print(f"ARMChip processing: {data}")
        return f"arm_processed_{data}"


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


class Monitor(OutputDevice):
    """External monitor — only an OutputDevice."""
    def output_data(self, data):
        print(f"Monitor displaying: {data}")


# ==========================================
# 3. BASE COMPUTER CLASS (High-Level Module)
#    DIP: depends on abstractions, not concrete classes
#    Getters and Setters: control and validate all attribute access
# ==========================================

class Computer:
    def __init__(self, color: str, dimensions: str,
                 input_device: InputDevice,
                 processor: Processor,
                 storage: Storage,
                 output_device: OutputDevice):

        # Using setters here so validation runs even during __init__
        self.color = color
        self.dimensions = dimensions
        self.input_device = input_device
        self.processor = processor
        self.storage = storage
        self.output_device = output_device

    # ---------- color ----------
    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        if not isinstance(value, str):
            raise TypeError("color must be a string")
        if len(value.strip()) == 0:
            raise ValueError("color cannot be empty")
        self._color = value

    # ---------- dimensions ----------
    @property
    def dimensions(self):
        return self._dimensions

    @dimensions.setter
    def dimensions(self, value):
        if not isinstance(value, str):
            raise TypeError("dimensions must be a string")
        if len(value.strip()) == 0:
            raise ValueError("dimensions cannot be empty")
        self._dimensions = value

    # ---------- input_device ----------
    @property
    def input_device(self):
        return self._input_device

    @input_device.setter
    def input_device(self, device):
        if not isinstance(device, InputDevice):
            raise TypeError("input_device must be an instance of InputDevice")
        self._input_device = device

    # ---------- processor ----------
    @property
    def processor(self):
        return self._processor

    @processor.setter
    def processor(self, device):
        if not isinstance(device, Processor):
            raise TypeError("processor must be an instance of Processor")
        self._processor = device

    # ---------- storage ----------
    @property
    def storage(self):
        return self._storage

    @storage.setter
    def storage(self, device):
        if not isinstance(device, Storage):
            raise TypeError("storage must be an instance of Storage")
        self._storage = device

    # ---------- output_device ----------
    @property
    def output_device(self):
        return self._output_device

    @output_device.setter
    def output_device(self, device):
        if not isinstance(device, OutputDevice):
            raise TypeError("output_device must be an instance of OutputDevice")
        self._output_device = device

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
        return (f"Computer(color={self._color}, dimensions={self._dimensions}, "
                f"input={type(self._input_device).__name__}, "
                f"processor={type(self._processor).__name__}, "
                f"storage={type(self._storage).__name__}, "
                f"output={type(self._output_device).__name__})")


# ==========================================
# 4. DESKTOP COMPUTER (Extends Computer)
#    LSP: DesktopComputer fully honours everything Computer promises
#    It ADDS swap_input_device because desktops genuinely support it
# ==========================================

class DesktopComputer(Computer):
    """
    LSP DEMO: DesktopComputer can do everything Computer can.
    It also adds swap_input_device() — desktops support external keyboard swaps.
    Anywhere a Computer is expected, a DesktopComputer works perfectly.
    """
    def swap_input_device(self, new_device: InputDevice):
        print(f"Swapping input device to {type(new_device).__name__}...")
        self.input_device = new_device   # goes through the setter — validated
        print("Input device swapped successfully.")


# ==========================================
# 5. LAPTOP (Extends Computer)
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
    def __init__(self, color, dimensions,
                 built_in_keyboard: InputDevice,
                 input_device: InputDevice,
                 processor, storage, output_device, battery_life: int):
        super().__init__(color, dimensions, input_device,
                         processor, storage, output_device)
        self.built_in_keyboard = built_in_keyboard  # fixed, laptop-only attribute
        self.battery_life = battery_life

    # ---------- built_in_keyboard ----------
    @property
    def built_in_keyboard(self):
        return self._built_in_keyboard

    @built_in_keyboard.setter
    def built_in_keyboard(self, device):
        if not isinstance(device, InputDevice):
            raise TypeError("built_in_keyboard must be an instance of InputDevice")
        self._built_in_keyboard = device

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

    def keyboard_input(self):
        """Explicitly use the built-in keyboard for input."""
        return self._built_in_keyboard.input_data()

    def touch_input(self):
        """Explicitly use the touch input device."""
        return self._input_device.input_data()

    def combined_input(self):
        """
        Collect input from BOTH the built-in keyboard and the touchscreen
        at the same time, and return them together as a dictionary.
        This reflects how a real laptop works — both inputs are always available.
        """
        keyboard_data = self._built_in_keyboard.input_data()
        touch_data    = self._input_device.input_data()
        return {
            "keyboard": keyboard_data,
            "touch":    touch_data
        }

    def combined_input(self):
        """
        Collect input from BOTH the built-in keyboard and the touchscreen
        at the same time and return them together as a dictionary.
        This reflects how a real laptop works — both inputs are always available.
        """
        keyboard_data = self._built_in_keyboard.input_data()
        touch_data    = self._input_device.input_data()
        return {
            "keyboard": keyboard_data,
            "touch":    touch_data
        }

    def __str__(self):
        return (f"Laptop(color={self._color}, dimensions={self._dimensions}, "
                f"battery={self._battery_life}hrs, "
                f"built_in_keyboard={type(self._built_in_keyboard).__name__}, "
                f"touch_input={type(self._input_device).__name__}, "
                f"processor={type(self._processor).__name__}, "
                f"storage={type(self._storage).__name__}, "
                f"output={type(self._output_device).__name__})")


# ==========================================
# 6. USAGE
# ==========================================

print("=" * 55)
print("        DESKTOP COMPUTER DEMO")
print("=" * 55)

# Build the parts
desktop_keyboard = Keyboard()
desktop_chip     = IntelChip()
desktop_memory   = InternalMemory()
desktop_monitor  = Monitor()

# Inject parts into DesktopComputer
my_desktop = DesktopComputer(
    color="Black",
    dimensions="Tower",
    input_device=desktop_keyboard,
    processor=desktop_chip,
    storage=desktop_memory,
    output_device=desktop_monitor
)

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

my_laptop = Laptop(
    color="Silver",
    dimensions="14-inch",
    built_in_keyboard=Keyboard(),   # fixed built-in keyboard
    input_device=laptop_screen,     # touchscreen as the second input
    processor=laptop_chip,
    storage=laptop_memory,
    output_device=laptop_screen,
    battery_life=12
)

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