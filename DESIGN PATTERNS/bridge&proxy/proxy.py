from abc import ABC, abstractmethod
from typing import Type


# Interface
class Image(ABC):
    @abstractmethod
    def display(self): pass


# Real Object (Heavy / Slow)
class RealImage(Image):
    def __init__(self, filename: str):
        self.filename = filename
        self._load_from_disk()            # Simulates an expensive operation

    def _load_from_disk(self):
        print(f"Loading {self.filename} from disk...")

    def display(self):
        print(f"Displaying {self.filename}")


# Proxy
class ProxyImage(Image):
    def __init__(
        self,
        filename: str,
        image_factory: Type[Image] = RealImage,
    ):
        self.filename = filename
        self._factory = image_factory
        self._real_image: Image | None = None

    def display(self):
        if self._real_image is None:
            # Lazy initialisation — only loads when first needed
            self._real_image = self._factory(self.filename)
        self._real_image.display()


# Demo
if __name__ == "__main__":
    # First call: triggers the expensive load
    image = ProxyImage("photo.jpg")
    image.display()    # Output: Loading photo.jpg from disk...
                       #         Displaying photo.jpg

    print()

    # Second call: uses cached real image — no reload
    image.display()    # Output: Displaying photo.jpg

    print()

    # Demonstrating DIP: inject a custom factory (e.g. for testing)
    class MockImage(Image):
        def __init__(self, filename: str):
            self.filename = filename
        def display(self):
            print(f"[MOCK] Displaying {self.filename}")

    mock_proxy = ProxyImage("test.jpg", image_factory=MockImage)
    mock_proxy.display()   # Output: [MOCK] Displaying test.jpg
