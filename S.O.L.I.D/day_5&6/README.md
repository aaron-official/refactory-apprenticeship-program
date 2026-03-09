# SOLID Principles — A Complete Guide with Python

This README explains every SOLID principle from scratch, shows the problem each one solves,
and maps each principle directly to the code in `solid_principles.py`.

---

## Table of Contents

1. [What is SOLID?](#what-is-solid)
2. [Project Overview](#project-overview)
3. [Project Structure](#project-structure)
4. [Foundation — Abstract Base Classes](#foundation--abstract-base-classes)
5. [S — Single Responsibility Principle](#s--single-responsibility-principle)
6. [O — Open/Closed Principle](#o--openclosed-principle)
7. [L — Liskov Substitution Principle](#l--liskov-substitution-principle)
8. [I — Interface Segregation Principle](#i--interface-segregation-principle)
9. [D — Dependency Inversion Principle](#d--dependency-inversion-principle)
10. [Bonus — Getters and Setters](#bonus--getters-and-setters)
11. [How Everything Connects](#how-everything-connects)
12. [Running the Code](#running-the-code)
13. [Expected Output](#expected-output)

---

## What is SOLID?

SOLID is a set of **5 design principles** for writing clean, maintainable, and scalable
object-oriented code. They were introduced by Robert C. Martin (nicknamed "Uncle Bob").

Each letter stands for one principle:

| Letter | Principle                       | One-Line Summary                                              |
|--------|---------------------------------|---------------------------------------------------------------|
| S      | Single Responsibility Principle | A class should have only one reason to change                 |
| O      | Open/Closed Principle           | Open for extension, closed for modification                   |
| L      | Liskov Substitution Principle   | Subclasses must be usable wherever their parent is used       |
| I      | Interface Segregation Principle | Never force a class to implement methods it does not need     |
| D      | Dependency Inversion Principle  | High-level modules depend on abstractions, not concrete classes|

These principles do not exist in isolation — they work together. Breaking one usually
leads to breaking others.

---

## Project Overview

The project models a **computer system** in Python. It includes:

- A base `Computer` class
- A `DesktopComputer` subclass that can swap peripherals
- A `Laptop` subclass with a built-in keyboard and touchscreen
- Separate classes for every hardware component (Keyboard, Monitor, etc.)
- Abstract interfaces that define what each component type must do

This setup is deliberately designed so that every SOLID principle is visible and
demonstrable through real code scenarios.

---

## Project Structure

```
solid_principles.py
│
├── INTERFACES (Abstractions)
│   ├── InputDevice         — anything that provides input
│   ├── Processor           — anything that processes data
│   ├── Storage             — anything that stores and retrieves data
│   ├── OutputDevice        — anything that displays output
│   └── Swappable           — anything that supports device swapping
│
├── CONCRETE CLASSES (Low-Level Modules)
│   ├── Keyboard            — implements InputDevice
│   ├── TouchScreen         — implements InputDevice + OutputDevice
│   ├── IntelChip           — implements Processor
│   ├── ARMChip             — implements Processor
│   ├── InternalMemory      — implements Storage
│   └── Monitor             — implements OutputDevice
│
└── CONTROLLERS (High-Level Modules)
    ├── Computer            — base class, orchestrates all components
    ├── DesktopComputer     — extends Computer, adds device swapping
    └── Laptop              — extends Computer, adds built-in keyboard + battery
```

---

## Foundation — Abstract Base Classes

Before diving into SOLID, you need to understand the tools used to enforce it.

### The Import

```python
from abc import ABC, abstractmethod
```

- `abc` is a built-in Python module — it stands for **Abstract Base Classes**
- `ABC` is a class you inherit from to make your class abstract (a blueprint, not a real object)
- `abstractmethod` is a decorator that marks a method as **required** — any subclass must implement it

### What is an Abstract Class?

```python
class InputDevice(ABC):
    @abstractmethod
    def input_data(self):
        pass
```

`InputDevice` is a **contract**. It says:

> *"Any class that calls itself an InputDevice must provide an `input_data()` method."*

You cannot create an `InputDevice` directly — it is not a real thing, it is a blueprint:

```python
device = InputDevice()   # ❌ TypeError: Can't instantiate abstract class
device = Keyboard()      # ✅ Keyboard IS an InputDevice — this works
```

The `pass` keyword inside `input_data()` means the body is intentionally empty.
The abstract class is only defining *what must exist*, not *how it works*.

### What does `@abstractmethod` do?

It enforces the contract. If a subclass forgets to implement a required method,
Python crashes immediately with a clear error:

```python
class BrokenDevice(InputDevice):
    pass   # forgot to implement input_data()

b = BrokenDevice()
# ❌ TypeError: Can't instantiate abstract class BrokenDevice
#    with abstract method input_data
```

This is Python's way of making sure every component delivers on its promise.

---

## S — Single Responsibility Principle

### Definition

> *A class should have one, and only one, reason to change.*

A class that does too many things becomes hard to understand, hard to test,
and hard to change without breaking something else.

### The Problem (without SRP)

Imagine cramming everything into one class:

```python
# ❌ This class does too much — violates SRP
class Computer:
    def receive_keyboard_input(self): ...
    def process_with_intel(self): ...
    def process_with_arm(self): ...
    def store_to_memory(self): ...
    def display_on_monitor(self): ...
    def display_on_touchscreen(self): ...
```

Every time any one component changes — say Intel updates its chip logic — you are
forced to edit the `Computer` class itself. The `Computer` class now has six reasons
to change. That is six times the risk of breaking something.

### How Our Code Follows SRP

Every class has exactly one job:

```python
class Keyboard(InputDevice):
    def input_data(self):              # ONLY job: receive keyboard input
        return "keyboard_raw_data"

class IntelChip(Processor):
    def process_data(self, data):      # ONLY job: process data
        return f"processed_{data}"

class InternalMemory(Storage):
    def store_data(self, data): ...    # ONLY job: manage memory
    def retrieve_data(self): ...

class Monitor(OutputDevice):
    def output_data(self, data): ...   # ONLY job: display output

class Computer:
    def input(self): ...               # ONLY job: orchestrate — delegate to components
    def process(self, data): ...
    def store(self, data): ...
    def output(self, data): ...
```

`Computer` itself does not receive keyboard input — it delegates that to `Keyboard`.
It does not process data — it delegates that to `IntelChip`. Each class has one
reason to change.

### Real-World Impact

If Intel releases a new chip, you only touch `IntelChip`. Nothing else changes.
If the keyboard hardware changes, you only touch `Keyboard`.
The `Computer` class never needs to know — it just calls `process_data()` and
trusts whatever chip is attached to handle it.

---

## O — Open/Closed Principle

### Definition

> *Software entities should be open for extension, but closed for modification.*

You should be able to add new behaviour by adding new code — **not** by editing
existing code that already works.

### The Problem (without OCP)

```python
# ❌ Every time you add a new chip, you edit Computer itself
class Computer:
    def process(self, data, chip_type):
        if chip_type == "intel":
            return f"intel_processed_{data}"
        elif chip_type == "arm":
            return f"arm_processed_{data}"
        elif chip_type == "amd":          # ← you keep editing this method
            return f"amd_processed_{data}"
```

Every new chip requires opening `Computer` and editing it. This risks breaking
existing functionality and violates OCP.

### How Our Code Follows OCP

The `Computer` class asks for a `Processor` — it does not care which one:

```python
class Computer:
    def process(self, data):
        return self.processor.process_data(data)   # delegates to whatever chip is injected
```

To add a new chip, you simply add a new class:

```python
# ✅ Add this without touching Computer at all
class AMDChip(Processor):
    def process_data(self, data):
        return f"amd_processed_{data}"
```

Then pass it in:

```python
my_computer = Computer(..., processor=AMDChip(), ...)
```

`Computer` is **closed for modification** — you never edit it. It is
**open for extension** — you can add `AMDChip`, `AppleM4`, or any other chip
just by creating a new class.

The same logic applies to every other component — `Keyboard`, `Monitor`, `ARMChip`,
`TouchScreen` are all extensions that required zero changes to `Computer`.

---

## L — Liskov Substitution Principle

### Definition

> *Objects of a subclass should be replaceable with objects of the parent class
> without breaking the program.*

In plain English: if your code works with a `Computer`, it must also work perfectly
with a `DesktopComputer` or a `Laptop` — without any surprises.

### The Problem (without LSP)

The classic violation is a subclass that **overrides a method and breaks the promise**
the parent made:

```python
# ❌ Laptop violates LSP — it claims to be a Computer but breaks its behaviour
class Laptop(Computer):
    def swap_input_device(self, new_device):
        raise Exception("Laptop keyboard is built-in, cannot be swapped!")
```

Now any code that works with `Computer` objects breaks when handed a `Laptop`:

```python
def upgrade_keyboard(computer: Computer, new_keyboard):
    computer.swap_input_device(new_keyboard)   # works for Computer...

upgrade_keyboard(my_desktop, Keyboard())   # ✅ works
upgrade_keyboard(my_laptop, Keyboard())    # ❌ CRASHES — LSP violated
```

### How Our Code Follows LSP

The solution is to **never promise what you cannot deliver**.

`swap_input_device` is placed in its own separate `Swappable` interface:

```python
class Swappable(ABC):
    @abstractmethod
    def swap_input_device(self, new_device):
        pass
```

`DesktopComputer` implements it because desktops genuinely support peripheral swapping:

```python
class DesktopComputer(Computer):              # ✅ fulfils everything Computer promises
    def swap_input_device(self, new_device: InputDevice):
        print(f"Swapping input device to {type(new_device).__name__}...")
        self.input_device = new_device
        print("Input device swapped successfully.")
```

`Laptop` does **not** implement `swap_input_device` at all:

```python
class Laptop(Computer):                       # ✅ fulfils everything Computer promises
    pass                                      # never claims it can swap — LSP safe
```

You can verify this:

```python
print(hasattr(my_laptop, 'swap_input_device'))   # False — never promised it
```

Anywhere a `Computer` is expected, both `DesktopComputer` and `Laptop` work
perfectly — they fulfil every method `Computer` defines. LSP is never broken.

### The Substitution Test

Ask yourself: *"Can I hand this subclass to any code that expects the parent,
without that code crashing or behaving unexpectedly?"*

```python
def run_computer(computer: Computer):
    raw = computer.input()
    processed = computer.process(raw)
    computer.store(processed)
    retrieved = computer.retrieve()
    computer.output(retrieved)

run_computer(my_desktop)   # ✅ works — DesktopComputer substitutes cleanly
run_computer(my_laptop)    # ✅ works — Laptop substitutes cleanly
```

Both pass the test. LSP is satisfied.

---

## I — Interface Segregation Principle

### Definition

> *A class should never be forced to implement an interface it does not use.*

Fat interfaces — interfaces with too many methods — force classes to implement
things that make no sense for them.

### The Problem (without ISP)

Imagine one giant interface for all computer components:

```python
# ❌ One fat interface — violates ISP
class ComputerComponent(ABC):
    @abstractmethod
    def input_data(self): pass

    @abstractmethod
    def process_data(self, data): pass

    @abstractmethod
    def store_data(self, data): pass

    @abstractmethod
    def retrieve_data(self): pass

    @abstractmethod
    def output_data(self, data): pass
```

Now every component is **forced to implement everything**:

```python
# ❌ Keyboard forced to implement methods that make no sense for it
class Keyboard(ComputerComponent):
    def input_data(self):
        return "keyboard_raw_data"    # ✅ makes sense

    def process_data(self, data):
        pass                          # ❌ a keyboard cannot process data

    def store_data(self, data):
        pass                          # ❌ a keyboard cannot store data

    def retrieve_data(self):
        pass                          # ❌ what does this even mean for a keyboard?

    def output_data(self, data):
        pass                          # ❌ a keyboard does not display things
```

The `Keyboard` class is polluted with four methods that do nothing and make no sense.
This is a maintenance nightmare.

### How Our Code Follows ISP

Interfaces are split into small, focused contracts:

```python
class InputDevice(ABC):       # only: input_data()
class Processor(ABC):         # only: process_data()
class Storage(ABC):           # only: store_data(), retrieve_data()
class OutputDevice(ABC):      # only: output_data()
class Swappable(ABC):         # only: swap_input_device()
```

Each class implements only the interface(s) that genuinely apply to it:

```python
class Keyboard(InputDevice):                   # only InputDevice — that is all it is
class Monitor(OutputDevice):                   # only OutputDevice — that is all it is
class IntelChip(Processor):                    # only Processor — that is all it is
class InternalMemory(Storage):                 # only Storage — that is all it is
class DesktopComputer(Computer):               # Computer + Swappable (can swap devices)
class Laptop(Computer):                        # Computer only (cannot swap — not Swappable)
```

### The TouchScreen — ISP's Best Demonstration

A touchscreen genuinely does two things: it receives touch input AND displays output.
So it correctly implements two interfaces:

```python
class TouchScreen(InputDevice, OutputDevice):
    def input_data(self):                         # ✅ touch input
        return "touch_raw_data"

    def output_data(self, data):                  # ✅ display output
        print(f"TouchScreen displaying: {data}")

    # process_data() ?  → NOT here. A screen cannot process.
    # store_data() ?    → NOT here. A screen cannot store.
```

You can verify this at runtime:

```python
ts = TouchScreen()
print(isinstance(ts, InputDevice))    # True  — it IS an input device
print(isinstance(ts, OutputDevice))   # True  — it IS an output device
print(isinstance(ts, Processor))      # False — it is NOT a processor
print(isinstance(ts, Storage))        # False — it is NOT storage
```

ISP says: implement exactly what you are, nothing more.

### The Laptop's Two Input Devices — ISP in `__init__`

A laptop has a physical built-in keyboard (which cannot be removed) and
a touchscreen (which handles both input and output). Rather than cramming
both into a single `input_device` slot inherited from `Computer`, `Laptop`
adds its own separate `built_in_keyboard` attribute:

```python
class Laptop(Computer):
    def __init__(self, ..., built_in_keyboard: InputDevice,
                 input_device: InputDevice, ...):
        super().__init__(..., input_device=input_device, ...)
        self.built_in_keyboard = built_in_keyboard   # laptop-only, fixed
```

Both are independently accessible:

```python
my_laptop.keyboard_input()    # routes through built_in_keyboard (Keyboard)
my_laptop.touch_input()       # routes through input_device (TouchScreen)
my_laptop.combined_input()    # collects from BOTH at the same time
```

`combined_input()` returns a dictionary so both sources are processed together:

```python
all_inputs = my_laptop.combined_input()
# Returns: {"keyboard": "keyboard_raw_data", "touch": "touch_raw_data"}

for source, data in all_inputs.items():
    processed = my_laptop.process(data)
    my_laptop.store(processed)
    my_laptop.output(processed)
```

---

## D — Dependency Inversion Principle

### Definition

> *High-level modules should not depend on low-level modules.
> Both should depend on abstractions.*

In other words: the `Computer` (high-level) should not be wired directly to
`Keyboard`, `IntelChip`, etc. (low-level). It should depend on the
abstract interfaces `InputDevice`, `Processor`, etc. instead.

### The Problem (without DIP)

```python
# ❌ Computer wired directly to specific hardware — violates DIP
class Computer:
    def __init__(self):
        self.input_device  = Keyboard()        # hardcoded — cannot change
        self.processor     = IntelChip()       # hardcoded — cannot change
        self.storage       = InternalMemory()  # hardcoded — cannot change
        self.output_device = Monitor()         # hardcoded — cannot change
```

This `Computer` is permanently tied to `Keyboard`, `IntelChip`, etc.
You cannot give it a touchscreen, swap in an ARM chip, or test it with mock components.
The high-level module is tightly coupled to specific low-level details.

### How Our Code Follows DIP

`Computer.__init__` accepts **abstract types**, not concrete ones:

```python
class Computer:
    def __init__(self, color: str, dimensions: str,
                 input_device: InputDevice,    # abstract — accepts ANY InputDevice
                 processor: Processor,         # abstract — accepts ANY Processor
                 storage: Storage,             # abstract — accepts ANY Storage
                 output_device: OutputDevice): # abstract — accepts ANY OutputDevice
```

The concrete objects are built **outside** and then **passed in**:

```python
# Build the specific parts
my_keyboard = Keyboard()
my_chip     = IntelChip()
my_memory   = InternalMemory()
my_monitor  = Monitor()

# Inject them into Computer
my_computer = Computer(
    color="Black",
    dimensions="Tower",
    input_device=my_keyboard,    # injected from outside
    processor=my_chip,           # injected from outside
    storage=my_memory,           # injected from outside
    output_device=my_monitor     # injected from outside
)
```

This pattern is called **Dependency Injection** — the computer does not build its
own parts. It receives them fully assembled from outside.

### Why This Matters

```python
# Swap the chip — no changes to Computer needed
my_computer = Computer(..., processor=ARMChip(), ...)

# Use a touchscreen instead of a monitor — no changes to Computer needed
my_computer = Computer(..., output_device=TouchScreen(), ...)

# Use a fake keyboard for testing — no changes to Computer needed
class FakeKeyboard(InputDevice):
    def input_data(self):
        return "test_data"

test_computer = Computer(..., input_device=FakeKeyboard(), ...)
```

`Computer` never knows or cares which specific class it receives — only that
it honours the abstract interface.

---

## Bonus — Getters and Setters

### The Problem Without Them

Without getters and setters, Python attributes are fully public:

```python
my_computer.color = 12345         # ❌ silently corrupts the object
my_computer.input_device = "hi"   # ❌ replaces a device with a plain string
```

Python will not complain. The object just ends up in a broken state.

### The Solution — Python's `@property`

Python uses the `@property` decorator to create getters and setters that
**look like normal attribute access** but actually run validation code behind the scenes.

```python
class Computer:
    # Getter — controls how you READ the value
    @property
    def color(self):
        return self._color

    # Setter — controls how you WRITE the value
    @color.setter
    def color(self, value):
        if not isinstance(value, str):
            raise TypeError("color must be a string")
        if len(value.strip()) == 0:
            raise ValueError("color cannot be empty")
        self._color = value    # only stored if it passes validation
```

### The Underscore Convention

Notice `self._color` instead of `self.color`. The `_` prefix is a Python
convention meaning "private — do not access directly from outside the class":

```python
my_computer._color    # ❌ technically possible but breaks the convention
my_computer.color     # ✅ correct — routes through the getter
```

### How It Looks in Use

Even though getters and setters are methods, Python makes them look like
plain attribute access — no brackets needed:

```python
print(my_computer.color)     # triggers getter silently
my_computer.color = "White"  # triggers setter silently, runs validation
```

### Validation in Action

```python
# Wrong type
my_computer.color = 999
# ❌ TypeError: color must be a string

# Empty string
my_computer.color = "   "
# ❌ ValueError: color cannot be empty

# Wrong device type
my_computer.input_device = "not a device"
# ❌ TypeError: input_device must be an instance of InputDevice

# All correct
my_computer.color = "White"  # ✅ passes
```

The device setters also **enforce the abstractions** — connecting DIP and
encapsulation together:

```python
@input_device.setter
def input_device(self, device):
    if not isinstance(device, InputDevice):    # enforces the abstraction
        raise TypeError("input_device must be an instance of InputDevice")
    self._input_device = device
```

---

## How Everything Connects

Here is how all five principles and getters/setters work together in one view:

```
INTERFACES (ABC)
    │   Defines the contract each component must honour
    │   ISP — each interface is small and focused
    │
    ▼
CONCRETE CLASSES
    │   Keyboard, TouchScreen, IntelChip, ARMChip,
    │   InternalMemory, Monitor
    │   SRP — each class has exactly one job
    │   OCP — new components can be added without touching existing code
    │   LSP — each class fully honours its interface contract
    │
    ▼
COMPUTER (High-Level)
    │   Accepts abstract types in __init__ — never hardcodes specific classes
    │   DIP — depends on InputDevice, Processor, etc., not on Keyboard, IntelChip
    │   Getters/Setters — validates and protects every attribute
    │
    ▼
DESKTOPCOMPUTER / LAPTOP
    │   Extend Computer cleanly — add only what genuinely applies
    │   LSP — both substitute for Computer without breaking anything
    │   ISP — Laptop never implements Swappable (it cannot swap devices)
```

---

## Running the Code

Make sure you have Python 3 installed, then run:

```bash
python3 solid_principles.py
```

No external libraries required — everything used (`abc`) is part of Python's
standard library.

---

## Expected Output

```
=======================================================
        DESKTOP COMPUTER DEMO
=======================================================
Computer(color=Black, dimensions=Tower, input=Keyboard, processor=IntelChip, storage=InternalMemory, output=Monitor)

Receiving input from Keyboard...
IntelChip processing: keyboard_raw_data
Storing data to Internal Memory...
Retrieving data from Internal Memory...
Monitor displaying: processed_keyboard_raw_data

--- Swapping keyboard on desktop ---
Swapping input device to TouchScreen...
Input device swapped successfully.
Receiving touch input from TouchScreen...
Monitor displaying: touch_raw_data

=======================================================
        LAPTOP DEMO
=======================================================
Laptop(color=Silver, dimensions=14-inch, battery=12hrs, built_in_keyboard=Keyboard, touch_input=TouchScreen, processor=ARMChip, storage=InternalMemory, output=TouchScreen)

--- Combined input from Keyboard + TouchScreen ---
Receiving input from Keyboard...
Receiving touch input from TouchScreen...

  [KEYBOARD]
ARMChip processing: keyboard_raw_data
...

  [TOUCH]
ARMChip processing: touch_raw_data
...

--- Laptop has no swap_input_device ---
hasattr swap_input_device: False

=======================================================
        GETTER / SETTER VALIDATION DEMO
=======================================================
TypeError caught: color must be a string
TypeError caught: input_device must be an instance of InputDevice
ValueError caught: color cannot be empty
Desktop color is now: White

=======================================================
        ISP DEMO
=======================================================
TouchScreen is InputDevice:  True
TouchScreen is OutputDevice: True
TouchScreen is Processor:    False
TouchScreen is Storage:      False
```

---

*Built for learning SOLID principles through a practical, real-world Python example.*