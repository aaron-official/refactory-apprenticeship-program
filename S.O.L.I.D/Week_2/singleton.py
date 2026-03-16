# ============================================================
# Singleton Pattern
# ============================================================
# The Singleton Pattern ensures that a class has only ONE
# instance throughout the entire lifetime of a program, and
# provides a global point of access to that instance.
#
# Common use cases:
#   - Database connection pools
#   - Configuration/settings managers
#   - Logging services
# ============================================================

class Singleton:
    # Class-level variable that holds the single shared instance.
    # It starts as None because no instance has been created yet.
    _instance = None

    def __new__(cls):
        """
        __new__ is called BEFORE __init__ when creating an object.
        It is responsible for actually creating (allocating) the object.

        Here we override it to:
          1. Check if an instance already exists.
          2. If NOT, create one using the default object creation (super().__new__).
          3. If YES, skip creation and return the existing one.
        This guarantees only one instance ever exists.
        """
        if cls._instance is None:
            # No instance exists yet — create one and store it
            cls._instance = super().__new__(cls)
        # Return the single shared instance (whether new or existing)
        return cls._instance


# ── Usage ────────────────────────────────────────────────────

s1 = Singleton()  # First call: instance is created and stored
s2 = Singleton()  # Second call: existing instance is returned, nothing new created

# Since both variables point to the SAME object in memory, this prints True
print(s1 is s2)  # True - same instance
