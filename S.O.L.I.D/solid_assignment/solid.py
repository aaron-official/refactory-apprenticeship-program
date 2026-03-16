from abc import ABC, abstractmethod

# --- INTERFACES (Abstractions) ---

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

# --- CONCRETE IMPLEMENTATIONS ---

class Keyboard(InputDevice):
    def input_data(self):
        print("Receiving input from Keyboard...")
        return "keyboard_raw_data"

    def __str__(self):
        return "Keyboard"

class TouchScreen(InputDevice, OutputDevice):
    def input_data(self):
        print("Receiving touch input from TouchScreen...")
        return "touch_raw_data"

    def output_data(self, data):
        print(f"TouchScreen displaying: {data}")

    def __str__(self):
        return "TouchScreen"

class IntelChip(Processor):
    def process_data(self, data):
        print(f"IntelChip processing: {data}")
        return f"processed_{data}"

    def __str__(self):
        return "IntelChip"

class AMDChip(Processor):
    def process_data(self, data):
        print(f"AMDChip processing: {data}")
        return f"amd_processed_{data}"

    def __str__(self):
        return "AMDChip"

class InternalMemory(Storage):
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

class SSDStorage(Storage):
    def __init__(self):
        self._disk = None

    def store_data(self, data):
        print("Writing data to SSD...")
        self._disk = data

    def retrieve_data(self):
        print("Reading data from SSD...")
        return self._disk

    def __str__(self):
        return "SSDStorage"

class Monitor(OutputDevice):
    def output_data(self, data):
        print(f"Monitor displaying: {data}")

    def __str__(self):
        return "Monitor"

class Projector(OutputDevice):
    def output_data(self, data):
        print(f"Projector projecting: {data}")

    def __str__(self):
        return "Projector"

# --- COMPUTER CLASS ---

class Computer:
    def __init__(self, color: str, dimensions: str, input_device: InputDevice,
                 processor: Processor, storage: Storage, output_device: OutputDevice):
        self._color = color
        self._dimensions = dimensions
        self._input_device = input_device
        self._processor = processor
        self._storage = storage
        self._output_device = output_device

    # --- Getters ---

    @property
    def color(self):
        return self._color

    @property
    def dimensions(self):
        return self._dimensions

    @property
    def input_device(self):
        return self._input_device

    @property
    def processor(self):
        return self._processor

    @property
    def storage(self):
        return self._storage

    @property
    def output_device(self):
        return self._output_device

    # --- Setters (allow swapping components AFTER instantiation) ---

    @color.setter
    def color(self, value):
        self._color = value

    @dimensions.setter
    def dimensions(self, value):
        self._dimensions = value

    @input_device.setter
    def input_device(self, value):
        self._input_device = value

    @processor.setter
    def processor(self, value):
        self._processor = value

    @storage.setter
    def storage(self, value):
        self._storage = value

    @output_device.setter
    def output_device(self, value):
        self._output_device = value

    # --- Operations ---

    def run_cycle(self):
        data = self.input_device.input_data()
        processed = self.processor.process_data(data)
        self.storage.store_data(processed)
        retrieved = self.storage.retrieve_data()
        self.output_device.output_data(retrieved)

    def __str__(self):
        return (f"Computer(color={self.color}, dimensions={self.dimensions}, "
                f"input={self.input_device}, processor={self.processor}, "
                f"storage={self.storage}, output={self.output_device})")


# --- USAGE DEMO ---
# ONE computer is created. Setters change its components after instantiation.
# Same computer — different behavior. That is subtype polymorphism.

computer = Computer(
    color="Midnight Blue",
    dimensions="Standard Tower",
    input_device=Keyboard(),
    processor=IntelChip(),
    storage=InternalMemory(),
    output_device=Monitor()
)

print("=" * 55)
print("INITIAL STATE — Intel + Keyboard + Monitor")
print("=" * 55)
print(computer)
computer.run_cycle()

# Use setters to swap the processor — no new computer created
print("\n" + "=" * 55)
print("AFTER SETTER — Swap to AMD processor")
print("=" * 55)
computer.processor = AMDChip()
print(computer)
computer.run_cycle()

# Use setters to swap input and output devices
print("\n" + "=" * 55)
print("AFTER SETTER — Swap to TouchScreen + Projector + SSD")
print("=" * 55)
computer.input_device  = TouchScreen()
computer.output_device = Projector()
computer.storage       = SSDStorage()
print(computer)
computer.run_cycle()

# Use getter to read a specific component
print("\n" + "=" * 55)
print("USING GETTER — Read current processor")
print("=" * 55)
print(f"Current processor: {computer.processor}")