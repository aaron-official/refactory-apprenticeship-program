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
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance



# Usage

s1 = Singleton()  
s2 = Singleton() 

print(s1 is s2)  
