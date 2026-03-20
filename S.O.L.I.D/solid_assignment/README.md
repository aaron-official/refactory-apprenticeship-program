# SOLID Principles in Computer Systems

This project demonstrates the application of the **SOLID Principles** in a modular computer system. These five design principles help keep software systems flexible, maintainable, and easy to scale.

---

## 🛠 What is S.O.L.I.D?

1.  **S - Single Responsibility Principle (SRP)**
2.  **O - Open/Closed Principle (OCP)**
3.  **L - Liskov Substitution Principle (LSP)**
4.  **I - Interface Segregation Principle (ISP)**
5.  **D - Dependency Inversion Principle (DIP)**

---

## 🏗 Breakdown of the Core Principles

### 1. Single Responsibility Principle (SRP)
**Goal**: A class should have only one reason to change.
In this project, every component has a single, well-defined job. The `Keyboard` only handles input; the `IntelChip` only handles processing.
```python
class Keyboard(InputDevice):
    def input_data(self):
        print("Receiving input from Keyboard...")
        return "keyboard_raw_data"
```

### 2. Open/Closed Principle (OCP)
**Goal**: Software entities should be open for extension but closed for modification.
The `Computer` class is designed to work with *any* processor or storage that follows the interface. To add an `AMDChip`, we don't need to change the `Computer` class code.
```python
class Computer:
    def __init__(self, ..., processor: Processor, ...):
        self._processor = processor
```

### 3. Liskov Substitution Principle (LSP)
**Goal**: Subclasses should be replaceable for their base classes.
Any `InputDevice` can be used by the `Computer` without it knowing the difference. Whether it's a `Keyboard` or a `TouchScreen`, the behavior remains consistent for the caller.
```python
# Both are interchangeable as InputDevices
computer.input_device = Keyboard()
computer.input_device = TouchScreen()
```

### 4. Interface Segregation Principle (ISP)
**Goal**: Many client-specific interfaces are better than one general-purpose interface.
We split our hardware into specific interfaces (`InputDevice`, `Processor`, `Storage`, `OutputDevice`) rather than one giant "Hardware" interface. This means a `Monitor` doesn't have to implement storage methods it doesn't need.
```python
class OutputDevice(ABC):
    @abstractmethod
    def output_data(self, data):
        pass
```

### 5. Dependency Inversion Principle (DIP)
**Goal**: Depend on abstractions, not concretions.
The `Computer` doesn't depend on "Intel" or "SSD" directly. It depends on the `Processor` and `Storage` interfaces. This "inverts" the dependency so high-level logic (the Computer) isn't forced to change when low-level hardware (the Chip) changes.
```python
# Computer depends on the abstraction 'Processor'
def __init__(self, ..., processor: Processor, ...):
```

---

## 📚 Learning Resources

### Diagrams & Visuals
- **Online Class Diagram**: [SOLID Principles Layout](https://app.diagrams.net/#G1Wce2xVE8jmtGnA9lLVw_QwfO60Bex1Qf#%7B%22pageId%22%3A%22Z9hdbjzqC8r6VXsUVuU8%22%7D)
- **Visual Representation**:
![SOLID Principles Class Diagram](./Solid%20Principles%20Class%20Diagram.png)

### Presentations
- **Google Slides**: [SOLID Principles Presentation](https://docs.google.com/presentation/d/1LVMYb4aF46xZ78lRqHYLBRbnoQe18AI1dBTfiLgG87s/edit?usp=sharing)
- **Local PPTX**: [SOLID_Principles.pptx](./SOLID_Principles.pptx)

---

> "SOLID principles are not laws; they are a mindset. They help us build systems that survive the test of time and change."
