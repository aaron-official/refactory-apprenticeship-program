# Singleton Design Pattern

## Overview
The **Singleton Design Pattern** is used to ensure that a class has **only one instance** throughout the entire life of a program. It also provides a single, global point of access to that one instance.

## Analogy: A TV Remote Control
Imagine a house with only one TV and only **one Remote Control**.
- No matter who in the family wants to change the channel, they all have to find and use that same, single remote. 
- You can't just "create" a second remote out of thin air; there is only one physical device that can talk to the TV.

In code, a Singleton works the same way: whenever you ask for the object, the system says, "Here's the one we already have," instead of building a new one.

## How the Code Works
1. **The Private Lock (`_instance`)**: The class has a secret variable that stores the one and only instance.
2. **The Constructor Override (`__new__`)**: Normally, calling `Singleton()` creates a new object. We "override" this to check:
   - "Do we already have an instance?"
   - If **No**: Create it and save it in the secret variable.
   - If **Yes**: Just return the one we already saved.
3. **Consistency**: Because it's always the same object, any data you save in it (like a `value`) is visible to everyone else who uses the Singleton.

## Code Snippets

### The Singleton Logic
```python
class Singleton:
    _instance = None  # The secret storage for the one instance

    def __new__(cls):
        # Only create a new object if one doesn't exist yet
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance
```

### The Usage
```python
# Both variables will point to the EXACT same object
obj1 = Singleton()
obj2 = Singleton()

print(obj1 is obj2)  # Output: True
```

## Learning Resources
### Diagrams
- **Online Diagram**: [Singleton Pattern Logic](https://app.diagrams.net/?src=about#G16N82Lm5CBlm4w7gHlV4D0y85aykI-tRz#%7B%22pageId%22%3A%22jpA-xZUqiL99wG0qCtew%22%7D)
- **Local PDF Reference**: [singeleton&strategy.pdf](./singeleton&strategy.pdf)

### Presentations
- **Google Slides**: [Singleton & Strategy Presentation](https://docs.google.com/presentation/d/1czLdGu-jWNQqcHLudkvtE30Ok-myi70BnWcnIwEZ4lQ/edit?usp=sharing)
- **Local PPTX**: [Singleton&strategy.pptx](./Singleton&strategy.pptx)
