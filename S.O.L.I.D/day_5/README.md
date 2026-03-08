# SOLID Principles in `solid.py`

This document explains how the five SOLID principles of object-oriented design are applied in the `solid.py` example.

## 1. Single Responsibility Principle (SRP)
**Goal:** A class should have one, and only one, reason to change.

**How it's used:** 
Our classes now have only one reason to change, as each handles a single, well-defined job.
- The `Keyboard`, `IntelChip`, `InternalMemory`, and `Monitor` classes only focus on their specific hardware tasks.
- The `Computer` class is solely responsible for coordinating the workflow between the components, not for building them or knowing how they physically operate.

## 2. Open/Closed Principle (OCP)
**Goal:** Software entities should be open for extension, but closed for modification.

**How it's used:**
Your software is now open for extension but closed for modification.
- If you want to add an `AMDChip` or a `Mouse`, you simply create new classes that inherit from `Processor` or `InputDevice`.
- You can pass these new components right into the `Computer` without ever needing to modify the `Computer` class's internal code.

## 3. Liskov Substitution Principle (LSP)
**Goal:** Subtypes must be substitutable for their base types.

**How it's used:**
Your subclasses are perfectly substitutable for their base types without breaking the program.
- The `Computer` class expects objects that follow the contracts set by the `InputDevice`, `Processor`, `Storage`, and `OutputDevice` abstract classes.
- Because `IntelChip` inherits from `Processor` and implements the required `process_data()` method, it acts as a flawless substitute for the `Processor` abstraction.

## 4. Interface Segregation Principle (ISP)
**Goal:** Clients should not be forced to depend on interfaces they do not use.

**How it's used:**
Clients are not forced to depend on interfaces or methods they do not use.
- Instead of creating one massive interface with methods for input, output, storage, and processing, we segregated them into four small, specific abstract base classes: `InputDevice`, `Processor`, `Storage`, and `OutputDevice`.
- Because of this, your `Monitor` class only has to implement `output_data()` and isn't forced to carry around empty, useless methods for storing or processing data.

## 5. Dependency Inversion Principle (DIP)
**Goal:** High-level modules should not depend on low-level modules. Both should depend on abstractions.

**How it's used:**
Your high-level module (`Computer`) no longer depends on low-level modules (`Keyboard`, `IntelChip`). Both now depend on abstractions.
- Instead of hard-coding the creation of an `IntelChip` inside the `Computer`, the `Computer` relies on the `Processor` abstraction.
- You achieve this using **Dependency Injection** by passing the initialized `my_keyboard`, `my_processor`, etc., into the `Computer` constructor from the outside.