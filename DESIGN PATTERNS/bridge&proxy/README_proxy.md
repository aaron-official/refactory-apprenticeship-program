# Proxy Design Pattern

## Overview
The **Proxy Design Pattern** provides a "surrogate" or a placeholder for another object. Its job is to control access to the original object, especially if that object is "heavy," expensive to load, or slow to respond. This is often called **Lazy Loading**.

## Analogy: A Personal Assistant
Think of a Busy Manager and their **Personal Assistant** (the Proxy). 
- If someone wants to talk to the Manager, they first talk to the Assistant.
- If the request is simple, the Assistant can handle it using things they already know (like the Manager's schedule).
- Only when there's a real need does the Assistant "bring in" the actual Manager.

This way, the Manager isn't constantly disturbed, and work keeps moving smoothly.

## How the Code Works
1. **The Shared Interface (`Image`)**: A rule that says both the Proxy and the Real Object must have a `display` method.
2. **The Real Object (`RealImage`)**: This represents a heavy file on your hard drive. Loading it takes time and resources.
3. **The Proxy (`ProxyImage`)**: This is a lightweight version that "waits" until you actually ask it to `display` for the first time.
4. **Lazy Initialization**: In the code, the `ProxyImage` doesn't load the real image until the first time `display()` is called. After that, it "remembers" it so it doesn't have to load it again!
5. **The Usage**: In the demo, you see that the first call triggers a "Loading..." message, but the second call is instant because the Proxy already has the real image ready.

## Code Snippets

### Lazy Initialization in the Proxy
```python
class ProxyImage(Image):
    def __init__(self, filename: str):
        self.filename = filename
        self._real_image = None  # Start with nothing (lightweight)

    def display(self):
        # Only load the heavy object when display is actually called
        if self._real_image is None:
            self._real_image = RealImage(self.filename)
        self._real_image.display()
```

### The Usage
```python
# This object is very fast to create because it's just a proxy
image = ProxyImage("photo.jpg")

# The heavy loading only happens now
image.display()

# The second call is instant because it's already loaded!
image.display()
```

## Learning Resources
### Diagrams
- **Online Diagram**: [Proxy Pattern Logic](https://app.diagrams.net/#G1hiaV4tORlANiCNWRc7vZAPKK00dx0BPM#%7B%22pageId%22%3A%22jfpDkuWQmhNvxBL-DCqG%22%7D)
- **Local PDF Reference**: [proxy&bridge.pdf](./proxy&bridge.pdf)

### Presentations
- **Google Slides**: [Proxy & Bridge Presentation](https://docs.google.com/presentation/d/1fUBS59iILGOX2Of8CKsa_OCkAjqiZa-xYCih_p5v-fo/edit?usp=sharing)
- **Local PPTX**: [proxy& bridge.pptx](./proxy&%20bridge.pptx)
