# Design Patterns

Welcome to the Design Patterns section! This guide is designed to onboard anyone to the world of design patterns, explaining what they are, why they matter, and providing a map of the most common solutions used in professional software development.

---

## 🚀 What are Design Patterns?

Imagine you're a builder. Instead of inventing a new way to build a door or a roof every single time, you use a **blueprint** that has worked for thousands of other houses.

In software, **Design Patterns** are exactly that: **blueprints for solving recurring coding problems.** They aren't finished pieces of code you can just copy-paste; they are descriptions or templates for how to structure your objects and classes to solve a particular problem in a way that is proven to be efficient and clean.

### Why Should You Use Them?
- **Stop Reinventing the Wheel**: Use solutions that have already been tested and refined by thousands of developers.
- **Common Language**: When you tell a teammate "I'm using a Singleton here," they instantly know how the code is structured without you explaining every line.
- **Better Code Structure**: They help you follow best practices (like making code easier to change later).

---

## 🛠 the Categories of Patterns

The most famous patterns come from a book by the "Gang of Four" (GoF) and are divided into three main buckets:

1.  **Creational**: How objects are created (e.g., ensuring you only have one of something).
2.  **Structural**: How objects and classes are assembled into larger structures (e.g., adding "wrappers" to things).
3.  **Behavioral**: How objects communicate and work together to get a job done.

---

## 📍 Patterns Covered in this Section

While there are many patterns, we focus on **7 core patterns** in this repository. Each linked folder below contains Python code and a detailed breakdown.

| Category | Pattern | Analogy | Description |
| :--- | :--- | :--- | :--- |
| **Creational** | [**Singleton**](./singleton&strategy/README_singleton.md) | A single TV Remote | Ensures only one instance of a class ever exists. |
| **Structural** | [**Decorator**](./observer&decorator/README_decorator.md) | Boda Accessories | Adds new features to an object "on the fly" by wrapping it. |
| | [**Bridge**](./bridge&proxy/README_bridge.md) | Universal Remote | Splits control logic from the actual hardware. |
| | [**Proxy**](./bridge&proxy/README_proxy.md) | Personal Assistant | Uses a placeholder to control access to a "heavy" object. |
| | [**Facade**](./facade/README_facade.md) | Starting a Car | Provides one simple button to run a complex system inside. |
| **Behavioral** | [**Strategy**](./singleton&strategy/README_strategy.md) | Picking a Route | Lets you swap the "way of doing things" at runtime. |
| | [**Observer**](./observer&decorator/README_observer.md) | SMS Alerts | Automatically notifies listeners when something changes. |

---

## 🌐 Other Common Design Patterns

Beyond the 7 covered above, there are **16 other classic patterns** you might encounter. Here is a brief look at some of the most popular ones:

### Creational
- **Factory Method**: Deferring the decision of which class to create to its subclasses.
- **Abstract Factory**: Creating whole families of related objects (like a set of Windows-style or Mac-style buttons).
- **Builder**: A step-by-step way to construct a very complex object.
- **Prototype**: Creating new objects by "cloning" an existing one.

### Structural
- **Adapter**: Making two incompatible interfaces work together (like a power plug adapter).
- **Composite**: Treating individual objects and "groups of objects" the same way (like files and folders).
- **Flyweight**: Saving memory by sharing small parts of many similar objects.

### Behavioral
- **Iterator**: A standard way to loop through a collection without knowing how it's stored.
- **State**: Letting an object change its behavior when its internal "mood" or state changes.
- **Command**: Turning a request into a stand-alone object (useful for "Undo" buttons).
- **Template Method**: Defining the "skeleton" of an algorithm but letting subclasses fill in the specific steps.
- **Mediator**: Reducing chaotic dependencies between objects by making them communicate through a central hub.
- **Memento**, **Chain of Responsibility**, **Interpreter**, **Visitor**.

---

> *"Design patterns are not about inventing something new; they're about recognizing the solutions that already exist in nature and applying them to your code."*
