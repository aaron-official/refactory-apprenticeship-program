
#CONCRETE COMPONENTS
class Keyboard:
    def input_data(self):
        # This prompts the actual user to type something on their physical keyboard
        user_typed_data = input("Please type something on the keyboard: ")

        # It returns whatever the user actually typed
        return user_typed_data

class IntelChip:
    def process_data(self, data):
        print("Process data using the intel chip")
        return f"processed_{data}"

class InternalMemory:
    def __init__(self):
        self._memory = None

    def store_data(self, data):
        print("Store data to internal memory")
        self._memory = data

    def retrieve_data(self):
        print("Retrieve data from internal memory")
        return self._memory

class Monitor:
    def output_data(self, data):
        print(f"Output data on a monitor: {data}")



#  CONTROLLER (The Computer)
# a class that delegates methods

class Computer:
    def __init__(self, color: str, dimensions: str):
        # Attributes
        self.color = color
        self.dimensions = dimensions
        
        # Components are attached through direct composition
        self.keyboard = Keyboard()
        self.intelChip = IntelChip()
        self.internalMemory = InternalMemory()
        self.monitor = Monitor()

    # Methods
    def input(self):
        return self.keyboard.input_data()

    def process(self, data):
        return self.intelChip.process_data(data)

    def store(self, data):
        self.internalMemory.store_data(data)

    def retrieve(self):
        return self.internalMemory.retrieve_data()

    def output(self, data):
        self.monitor.output_data(data)



#USAGE EXAMPLE


# Creating the computer
my_computer = Computer(color="Black", dimensions="15-inch")

# Running the computer's methods
data = my_computer.input()
processed = my_computer.process(data)
my_computer.store(processed)
retrieved_data = my_computer.retrieve()
my_computer.output(retrieved_data)