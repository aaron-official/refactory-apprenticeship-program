# SOLID Principles — A Complete Guide with Python

This README explains every SOLID principle from scratch, shows the problem each one solves,
and maps each principle directly to the code in `solid_principles.py`.

Beyond SOLID, the code also demonstrates several **clean code patterns** that eliminate
common code smells: **Python Descriptors**, **Parameter Objects**, **`__str__` delegation**,
and a careful **LSP fix** in the `Laptop` class.

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
10. [Clean Code Pattern — Descriptors](#clean-code-pattern--descriptors)
11. [Clean Code Pattern — Parameter Objects](#clean-code-pattern--parameter-objects)
12. [Clean Code Pattern — `__str__` Delegation](#clean-code-pattern--__str__-delegation)
13. [How Everything Connects](#how-everything-connects)
14. [Running the Code](#running-the-code)
15. [Expected Output](#expected-output)

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
- **Descriptors** that replace repetitive getter/setter boilerplate
- **Parameter Objects** (`@dataclass`) that bundle constructor arguments cleanly
- **`__str__` methods** on each component so objects describe themselves

This setup is deliberately designed so that every SOLID principle and every clean code
pattern is visible and demonstrable through real code scenarios.

---

## Project Structure

```
solid_principles.py
│
├── IMPORTS
│   ├── abc (ABC, abstractmethod)     — for abstract interfaces
│   └── dataclasses (dataclass)       — for parameter objects
│
├── 1. INTERFACES (Abstractions)
│   ├── InputDevice         — anything that provides input
│   ├── Processor           — anything that processes data
│   ├── Storage             — anything that stores and retrieves data
│   ├── OutputDevice        — anything that displays output
│   └── Swappable           — anything that supports device swapping
│
├── 2. CONCRETE CLASSES (Low-Level Modules)
│   ├── Keyboard            — implements InputDevice
│   ├── TouchScreen         — implements InputDevice + OutputDevice
│   ├── IntelChip           — implements Processor
│   ├── ARMChip             — implements Processor
│   ├── InternalMemory      — implements Storage
│   └── Monitor             — implements OutputDevice
│
├── 3. DESCRIPTORS (Reusable Validation)
│   ├── ValidatedDevice     — type-checks hardware components
│   └── ValidatedString     — validates non-empty strings
│
├── 4. PARAMETER OBJECTS (Eliminate Long Parameter Lists)
│   ├── ComputerSpecs       — bundles the 6 base Computer fields
│   └── LaptopSpecs         — extends ComputerSpecs with laptop-specific fields
│
├── 5–7. CONTROLLERS (High-Level Modules)
│   ├── Computer            — base class, orchestrates all components
│   ├── DesktopComputer     — extends Computer, adds device swapping (Swappable)
│   └── Laptop              — extends Computer, adds built-in keyboard + battery
│
└── 8. USAGE / DEMOS
    ├── Desktop Computer Demo
    ├── Laptop Demo
    ├── Swappable Interface Check
    ├── Getter / Setter Validation Demo
    └── ISP Demo
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

Then pass it in via the specs object:

```python
my_specs = ComputerSpecs(..., processor=AMDChip(), ...)
my_computer = Computer(my_specs)
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

The solution has two parts:

**Part 1 — Separate the `Swappable` interface:**

`swap_input_device` is placed in its own separate `Swappable` interface so only
classes that genuinely support swapping implement it:

```python
class Swappable(ABC):
    @abstractmethod
    def swap_input_device(self, new_device):
        pass

class DesktopComputer(Computer, Swappable):   # ✅ implements Swappable
    def swap_input_device(self, new_device: InputDevice):
        self.input_device = new_device

class Laptop(Computer):                       # ✅ does NOT implement Swappable
    pass                                      # never claims it can swap — LSP safe
```

You can verify the interface at runtime:

```python
isinstance(my_desktop, Swappable)   # True  — desktop CAN swap
isinstance(my_laptop, Swappable)    # False — laptop CANNOT swap
```

**Part 2 — Override `input()` in `Laptop` (The Subtle LSP Fix):**

The base `Computer.input()` returns data from `self.input_device`. But a Laptop has
**two** input devices (built-in keyboard + touchscreen). If `Laptop` inherited
`input()` unchanged, calling `my_laptop.input()` would silently only return the
touchscreen data, completely ignoring the keyboard — **unexpected behaviour** for
any code expecting a `Computer`.

The fix is to override `input()` so it honours the contract fully:

```python
class Laptop(Computer):
    def input(self):
        """Fulfills the base class contract by returning the laptop's combined input."""
        return self.combined_input()
```

Now `my_laptop.input()` returns **all** input (keyboard + touch), which is what a
caller would reasonably expect from any `Computer`.

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
run_computer(my_laptop)    # ✅ works — Laptop substitutes cleanly (returns combined input)
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
class DesktopComputer(Computer, Swappable):    # Computer + Swappable (can swap devices)
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
    built_in_keyboard = ValidatedDevice(InputDevice, "built_in_keyboard")

    def __init__(self, specs: LaptopSpecs):
        super().__init__(specs)
        self.built_in_keyboard = specs.built_in_keyboard   # laptop-only, fixed
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

`Computer.__init__` accepts a `ComputerSpecs` object whose fields are typed as
**abstract types**, not concrete ones:

```python
@dataclass
class ComputerSpecs:
    color: str
    dimensions: str
    input_device: InputDevice    # abstract — accepts ANY InputDevice
    processor: Processor         # abstract — accepts ANY Processor
    storage: Storage             # abstract — accepts ANY Storage
    output_device: OutputDevice  # abstract — accepts ANY OutputDevice

class Computer:
    def __init__(self, specs: ComputerSpecs):
        self.input_device = specs.input_device
        self.processor = specs.processor
        ...
```

The concrete objects are built **outside** and then **passed in** via the specs:

```python
# Build the specific parts
my_keyboard = Keyboard()
my_chip     = IntelChip()
my_memory   = InternalMemory()
my_monitor  = Monitor()

# Bundle into a specs object and inject
desktop_specs = ComputerSpecs(
    color="Black",
    dimensions="23-inch",
    input_device=my_keyboard,
    processor=my_chip,
    storage=my_memory,
    output_device=my_monitor
)

my_desktop = DesktopComputer(desktop_specs)
```

This pattern is called **Dependency Injection** — the computer does not build its
own parts. It receives them fully assembled from outside.

### Why This Matters

```python
# Swap the chip — no changes to Computer needed
specs = ComputerSpecs(..., processor=ARMChip(), ...)

# Use a touchscreen instead of a monitor — no changes to Computer needed
specs = ComputerSpecs(..., output_device=TouchScreen(), ...)

# Use a fake keyboard for testing — no changes to Computer needed
class FakeKeyboard(InputDevice):
    def input_data(self):
        return "test_data"

specs = ComputerSpecs(..., input_device=FakeKeyboard(), ...)
```

`Computer` never knows or cares which specific class it receives — only that
it honours the abstract interface.

---

## Clean Code Pattern — Descriptors

### The Problem: Boilerplate Getter/Setter Code

Without descriptors, protecting every attribute requires ~10 lines of repetitive
`@property` and `@setter` code per attribute:

```python
# ❌ ~50 lines of nearly identical getter/setter blocks
class Computer:
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

    @property
    def dimensions(self):           # same pattern repeated again...
        return self._dimensions

    @dimensions.setter
    def dimensions(self, value):    # ...and again for every attribute
        if not isinstance(value, str):
            raise TypeError("dimensions must be a string")
        ...
```

This bloats the class with ~50 lines of nearly identical code. The actual business
logic gets buried under boilerplate.

### The Solution: Python Descriptors

A descriptor is a class that defines `__get__` and `__set__` methods. When you use
it as a **class variable**, Python automatically routes attribute access through
the descriptor's methods.

We created two reusable descriptors:

**`ValidatedDevice`** — ensures a value is an instance of a specific abstract type:

```python
class ValidatedDevice:
    def __init__(self, expected_type, name):
        self.expected_type = expected_type
        self.name = f"_{name}"            # stores as _input_device, _processor, etc.

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self                   # when accessed from the class itself
        return getattr(obj, self.name)    # returns the stored value

    def __set__(self, obj, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(f"Must be an instance of {self.expected_type.__name__}")
        setattr(obj, self.name, value)    # stores only if valid
```

**`ValidatedString`** — ensures a value is a non-empty string:

```python
class ValidatedString:
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
```

### How They Are Used

Descriptors are declared as **class-level variables** in `Computer`:

```python
class Computer:
    # 6 lines replace ~50 lines of property/setter boilerplate!
    color = ValidatedString("color")
    dimensions = ValidatedString("dimensions")
    input_device = ValidatedDevice(InputDevice, "input_device")
    processor = ValidatedDevice(Processor, "processor")
    storage = ValidatedDevice(Storage, "storage")
    output_device = ValidatedDevice(OutputDevice, "output_device")

    def __init__(self, specs: ComputerSpecs):
        # Each assignment triggers the descriptor's __set__ → validation runs automatically
        self.color = specs.color
        self.input_device = specs.input_device
        ...
```

And in `Laptop`, the same pattern validates the additional attribute:

```python
class Laptop(Computer):
    built_in_keyboard = ValidatedDevice(InputDevice, "built_in_keyboard")
```

### How It Feels in Use

Even though descriptors are classes with `__get__` and `__set__`, Python makes them
feel like ordinary attributes — no brackets needed:

```python
print(my_desktop.color)        # triggers ValidatedString.__get__ silently
my_desktop.color = "White"     # triggers ValidatedString.__set__ → validates → stores
my_desktop.color = 999         # ❌ TypeError: color must be a string
my_desktop.color = "   "       # ❌ ValueError: color cannot be empty

my_desktop.input_device = "x"  # ❌ TypeError: Must be an instance of InputDevice
```

### Why Descriptors Matter

| Without Descriptors          | With Descriptors                   |
|------------------------------|------------------------------------|
| ~10 lines per attribute      | 1 line per attribute               |
| Copy-paste validation logic  | Write validation logic **once**    |
| Easy to forget in new attrs  | Hard to forget — just add one line |
| Business logic buried        | Clean, focused `__init__`          |

---

## Clean Code Pattern — Parameter Objects

### The Problem: Long Parameter Lists

The original `Computer.__init__` took **6 positional arguments**, and `Laptop.__init__`
took **8**. Passing this many arguments is error-prone — you could accidentally swap
the positions of `processor` and `storage` without Python complaining:

```python
# ❌ Easy to accidentally swap arguments
my_desktop = Computer("Black", "23-inch", keyboard, chip, memory, monitor)
#                                                   ^^^^  ^^^^^^
#                                    Did I swap processor and storage? Who knows!
```

### The Solution: `@dataclass` as a Parameter Object

Python's `@dataclass` decorator (from the `dataclasses` module) automatically
generates `__init__`, `__repr__`, and other methods for you. We use it to bundle
all constructor arguments into a single, named object:

```python
from dataclasses import dataclass

@dataclass
class ComputerSpecs:
    """Bundles the 6 constructor args for Computer into one clean object."""
    color: str
    dimensions: str
    input_device: InputDevice
    processor: Processor
    storage: Storage
    output_device: OutputDevice
```

For `Laptop`, we extend it with laptop-specific fields:

```python
@dataclass
class LaptopSpecs(ComputerSpecs):
    """Extends ComputerSpecs with laptop-specific fields."""
    built_in_keyboard: InputDevice = None
    battery_life: int = 0
```

### How They Are Used

Now constructors accept a **single specs object** instead of many positional args:

```python
class Computer:
    def __init__(self, specs: ComputerSpecs):
        self.color = specs.color
        self.dimensions = specs.dimensions
        self.input_device = specs.input_device
        ...

class Laptop(Computer):
    def __init__(self, specs: LaptopSpecs):
        super().__init__(specs)                         # base fields go up to Computer
        self.built_in_keyboard = specs.built_in_keyboard
        self.battery_life = specs.battery_life
```

And callers use **named keyword arguments**, making it impossible to accidentally
swap fields:

```python
# ✅ Named fields — you cannot accidentally swap processor and storage
desktop_specs = ComputerSpecs(
    color="Black",
    dimensions="23-inch",
    input_device=desktop_keyboard,
    processor=desktop_chip,          # clearly labeled
    storage=desktop_memory,          # clearly labeled
    output_device=desktop_monitor
)

my_desktop = DesktopComputer(desktop_specs)
```

### Why Parameter Objects Matter

| Without Parameter Object         | With Parameter Object              |
|----------------------------------|------------------------------------|
| 6–8 positional arguments         | 1 named specs object               |
| Easy to mix up argument order    | Named fields prevent mistakes      |
| Constructor signature is noisy   | Constructor is clean and simple    |
| Hard to extend (add more args)   | Easy to extend (add field to dataclass) |

---

## Clean Code Pattern — `__str__` Delegation

### The Problem: Tightly Coupled String Representations

The original `__str__` method used `type(self._processor).__name__` to display
component names. This creates tight coupling — if you later wrap a component
in a proxy or decorator, the `__str__` output would break or show confusing
class names like `ProcessorProxy` instead of `IntelChip`.

```python
# ❌ Tightly coupled to exact class names
def __str__(self):
    return f"processor={type(self._processor).__name__}"
    # Would break if _processor is wrapped in a proxy or decorator
```

### The Solution: Let Components Describe Themselves

Every concrete class now has its own `__str__` method:

```python
class Keyboard(InputDevice):
    def __str__(self):
        return "Keyboard"

class IntelChip(Processor):
    def __str__(self):
        return "IntelChip"

class Monitor(OutputDevice):
    def __str__(self):
        return "Monitor"
```

And `Computer.__str__` simply calls `str()` on each component (which Python does
automatically when you use an object inside an f-string):

```python
class Computer:
    def __str__(self):
        return (f"Computer(color={self.color}, dimensions={self.dimensions}, "
                f"input={self.input_device}, "        # calls Keyboard.__str__()
                f"processor={self.processor}, "       # calls IntelChip.__str__()
                f"storage={self.storage}, "            # calls InternalMemory.__str__()
                f"output={self.output_device})")       # calls Monitor.__str__()
```

Now if a component is wrapped in a proxy or decorator, it can override `__str__`
to return something sensible — and `Computer` never needs to change.

---

## How Everything Connects

Here is how all five SOLID principles and all three clean code patterns work together:

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
    │   __str__ — each component describes itself (decoupled)
    │
    ▼
DESCRIPTORS
    │   ValidatedDevice, ValidatedString
    │   Replace ~50 lines of repetitive getter/setter boilerplate
    │   Write validation logic once, reuse everywhere
    │
    ▼
PARAMETER OBJECTS
    │   ComputerSpecs, LaptopSpecs (@dataclass)
    │   Bundle constructor args into named objects
    │   Prevent accidental argument swaps
    │
    ▼
COMPUTER (High-Level)
    │   Accepts ComputerSpecs in __init__ — never hardcodes specific classes
    │   DIP — depends on InputDevice, Processor, etc., not on Keyboard, IntelChip
    │   Descriptors validate every field on assignment
    │
    ▼
DESKTOPCOMPUTER / LAPTOP
    │   Extend Computer cleanly — add only what genuinely applies
    │   LSP — both substitute for Computer without breaking anything
    │   LSP — Laptop overrides input() to honour the contract fully
    │   ISP — Laptop never implements Swappable (it cannot swap devices)
```

---

## Running the Code

Make sure you have Python 3 installed, then run:

```bash
python solid_principles.py
```

No external libraries required — everything used (`abc`, `dataclasses`) is part of
Python's standard library.

---

## Expected Output

```
=======================================================
        DESKTOP COMPUTER DEMO
=======================================================
Computer(color=Black, dimensions=23-inch, input=Keyboard, processor=IntelChip, storage=InternalMemory, output=Monitor)

Receiving input from Keyboard...
IntelChip processing: keyboard_raw_data
Storing data to Internal Memory...
Retrieving data from Internal Memory...
Monitor displaying: processed_keyboard_raw_data

--- Swapping keyboard on desktop ---
Swapping input device to TouchScreen...
Input device swapped successfully.
Receiving touch input from TouchScreen...
TouchScreen displaying: touch_raw_data

=======================================================
        LAPTOP DEMO
=======================================================
Laptop(color=Silver, dimensions=14-inch, battery=12hrs, built_in_keyboard=Keyboard, touch_input=TouchScreen, processor=ARMChip, storage=InternalMemory, output=TouchScreen)

--- Combined input from Keyboard + TouchScreen ---
Receiving input from Keyboard...
Receiving touch input from TouchScreen...

  [KEYBOARD]
ARMChip processing: keyboard_raw_data
Storing data to Internal Memory...
Retrieving data from Internal Memory...
TouchScreen displaying: arm_processed_keyboard_raw_data

  [TOUCH]
ARMChip processing: touch_raw_data
Storing data to Internal Memory...
Retrieving data from Internal Memory...
TouchScreen displaying: arm_processed_touch_raw_data

--- Laptop has no swap_input_device ---
hasattr swap_input_device: False

--- Swappable interface check ---
DesktopComputer is Swappable: True
Laptop is Swappable:          False

=======================================================
        GETTER / SETTER VALIDATION DEMO
=======================================================

--- Trying to set color to an integer ---
TypeError caught: color must be a string

--- Trying to pass a string as input_device ---
TypeError caught: Must be an instance of InputDevice

--- Trying to set an empty color ---
ValueError caught: color cannot be empty

--- Valid color change ---
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

*Built for learning SOLID principles and clean code patterns through a practical, real-world Python example.*