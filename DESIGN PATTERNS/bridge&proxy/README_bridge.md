# Bridge Design Pattern

## Overview
The **Bridge Design Pattern** is used to split a large class or a set of closely related classes into two separate hierarchies—**Abstraction** and **Implementation**—which can be developed independently. It "bridges" them together so they can work as a pair without being permanently stuck to each other.

## Analogy: A Universal Remote Control
Think of a **Remote Control** (the Abstraction) and a **TV** (the Implementation).
- The Remote has buttons like `toggle_power`.
- The TV handles the actual electronics to turn on or off.

If you want a new "Advanced Remote" with a `mute` button, you don't need to rebuild the TV. If you buy a "Radio" instead of a TV, you don't need to buy a new Remote. The Remote (the control) and the Device (the hardware) are independent, but they are "bridged" so they can talk to each other.

## How the Code Works
1. **The Device Interface**: A blueprint that says every device must have `enable`, `disable`, and `set_volume`.
2. **The Hardware (`TV`, `Radio`)**: These are the actual "machines" that follow the Device blueprint.
3. **The Remote (`RemoteControl`)**: This holds a reference (a bridge) to a device. It doesn't know *what* the device is, only that it follows the blueprint.
4. **The Advanced Remote**: This adds new buttons (like `mute`) by using the existing functions of the bridged device.
5. **The Power of the Bridge**: You can give a `BasicRemote` to a `TV`, or an `AdvancedRemote` to a `Radio`. Any remote works with any device because of the bridge!

## Code Snippets

### The Abstraction (The Remote)
```python
class RemoteControl:
    def __init__(self, device: Device):
        # This is the bridge—it connects the Remote back to a Device
        self.device = device

    def toggle_power(self):
        if self.device.is_enabled():
            self.device.disable()
        else:
            self.device.enable()
```

### The Usage
```python
# Create the machine (Implementor)
sony_tv = TV()

# Create the remote (Abstraction) and bridge it to the TV
basic_remote = RemoteControl(sony_tv)

# Use the remote—it triggers the TV behind the scenes
basic_remote.toggle_power()
```

## Learning Resources
### Diagrams
- **Online Diagram**: [Bridge Pattern Logic](https://app.diagrams.net/#G1hiaV4tORlANiCNWRc7vZAPKK00dx0BPM#%7B%22pageId%22%3A%22DRqMxTAWoe1h_xrDT3bL%22%7D)
- **Local PDF Reference**: [proxy&bridge.pdf](./proxy&bridge.pdf)

### Presentations
- **Google Slides**: [Proxy & Bridge Presentation](https://docs.google.com/presentation/d/1fUBS59iILGOX2Of8CKsa_OCkAjqiZa-xYCih_p5v-fo/edit?usp=sharing)
- **Local PPTX**: [proxy& bridge.pptx](./proxy&%20bridge.pptx)
