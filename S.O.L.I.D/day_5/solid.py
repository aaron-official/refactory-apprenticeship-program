from abc import ABC, abstractmethod

# 1. Interfaces (Abstractions)

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

# 2. Concrete Implementations (Low-Level Modules)

class Keyboard(InputDevice):
    def input_data(self):
        print("Receiving input from Keyboard...")
        return "raw_data"
    
class IntelChip(Processor):
    def process_data(self, data):
        print(f"IntelChip processing: {data}")
        return f"processed_{data}"

class InternalMemory(Storage):
    def __init__(self):
        self._memory = None

    def store_data(self, data):
        print("Storing data to Internal Memory...")
        self._memory = data

    def retrieve_data(self):
        print("Retrieving data from Internal Memory...")
        return self._memory
    
class Monitor(OutputDevice):
    def output_data(self, data):
        print(f"Monitor displaying: {data}")

# 3. Controller (The Computer)

class Computer:
    def __init__(self, color: str, dimensions: str, 
                 input_device: InputDevice, processor: Processor, 
                 storage: Storage, output_device: OutputDevice):
        self.color = color
        self.dimensions = dimensions
        self.input_device = input_device
        self.processor = processor
        self.storage = storage
        self.output_device = output_device

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


# USAGE EXAMPLE

# Creating components
my_keyboard = Keyboard()
my_processor = IntelChip()
my_memory = InternalMemory()
my_monitor = Monitor()

# Creating the computer with Dependency Injection
my_computer = Computer(
    color="Black", 
    dimensions="15-inch", 
    input_device=my_keyboard, 
    processor=my_processor,
    storage=my_memory,
    output_device=my_monitor
)

# Operating the computer
raw_data = my_computer.input()
processed_data = my_computer.process(raw_data)
my_computer.store(processed_data)
retrieved = my_computer.retrieve()
my_computer.output(retrieved)
