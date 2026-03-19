from abc import ABC, abstractmethod


# Implementor Interface
class Device(ABC):
    @abstractmethod
    def is_enabled(self) -> bool: pass

    @abstractmethod
    def enable(self): pass

    @abstractmethod
    def disable(self): pass

    @abstractmethod
    def set_volume(self, level: int): pass


# Concrete Implementor A
class TV(Device):
    def __init__(self):
        self._enabled = False

    def is_enabled(self) -> bool:
        return self._enabled

    def enable(self):
        self._enabled = True
        print("TV: Power ON")

    def disable(self):
        self._enabled = False
        print("TV: Power OFF")

    def set_volume(self, level: int):
        print(f"TV: Volume set to {level}")


# Concrete Implementor B
class Radio(Device):
    def __init__(self):
        self._enabled = False

    def is_enabled(self) -> bool:
        return self._enabled

    def enable(self):
        self._enabled = True
        print("Radio: Power ON")

    def disable(self):
        self._enabled = False
        print("Radio: Power OFF")

    def set_volume(self, level: int):
        print(f"Radio: Volume set to {level}")


# Abstraction
class RemoteControl:
    def __init__(self, device: Device):
        self.device = device

    def toggle_power(self):
        if self.device.is_enabled():
            self.device.disable()
        else:
            self.device.enable()


# Refined Abstraction
class AdvancedRemoteControl(RemoteControl):
    def mute(self):
        print("Remote: Muting the device...")
        self.device.set_volume(0)


# Demo
if __name__ == "__main__":
    # TV starts OFF → toggle turns it ON
    sony_tv = TV()
    basic_remote = RemoteControl(sony_tv)
    basic_remote.toggle_power()      # Output: TV: Power ON
    basic_remote.toggle_power()      # Output: TV: Power OFF

    print()

    # Radio starts OFF → toggle turns it ON, then mute
    digital_radio = Radio()
    pro_remote = AdvancedRemoteControl(digital_radio)
    pro_remote.toggle_power()        # Output: Radio: Power ON
    pro_remote.mute()                # Output: Remote: Muting the device...
                                     #         Radio: Volume set to 0
