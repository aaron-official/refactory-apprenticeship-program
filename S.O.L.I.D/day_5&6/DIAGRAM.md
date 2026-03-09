# SOLID Principles — Class Diagram

```
                                    ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
                                    │                                   «abstract»                                                    │
                                    │                                    Computer                                                     │
                                    ├─────────────────────────────────────────────────────────────────────────────────────────────────┤
                                    │  - _color         : str                                                                         │
                                    │  - _dimensions    : str                                                                         │
                                    │  - _input_device  : InputDevice                                                                 │
                                    │  - _processor     : Processor                                                                   │
                                    │  - _storage       : Storage                                                                     │
                                    │  - _output_device : OutputDevice                                                                │
                                    ├─────────────────────────────────────────────────────────────────────────────────────────────────┤
                                    │  + color          : str          «property»                                                     │
                                    │  + dimensions     : str          «property»                                                     │
                                    │  + input_device   : InputDevice  «property»                                                     │
                                    │  + processor      : Processor    «property»                                                     │
                                    │  + storage        : Storage      «property»                                                     │
                                    │  + output_device  : OutputDevice «property»                                                     │
                                    │  + input()                                                                                      │
                                    │  + process(data)                                                                                │
                                    │  + store(data)                                                                                  │
                                    │  + retrieve()                                                                                   │
                                    │  + output(data)                                                                                 │
                                    │  + __str__()                                                                                    │
                                    └──────────────────────────┬──────────────────────────────────────────────────────────────────────┘
                                                               │
                                              extends          │         extends
                          ┌────────────────────────────────────┴───────────────────────────────────────┐
                          ▼                                                                             ▼
      ┌───────────────────────────────────────────┐                      ┌────────────────────────────────────────────────┐
      │               DesktopComputer             │                      │                    Laptop                      │
      ├───────────────────────────────────────────┤                      ├────────────────────────────────────────────────┤
      │  (inherits all Computer attributes)       │                      │  - _battery_life : int                         │
      ├───────────────────────────────────────────┤                      ├────────────────────────────────────────────────┤
      │  + swap_input_device(new_device)          │                      │  + battery_life  : int  «property»             │
      └───────────────────────────────────────────┘                      │  + __str__()                                   │
                          │                                               └────────────────────────────────────────────────┘
                          │ implements
                          ▼
      ┌───────────────────────────────────────────┐
      │             «abstract»                    │
      │              Swappable                    │
      ├───────────────────────────────────────────┤
      │  + swap_input_device(new_device)*         │
      └───────────────────────────────────────────┘




                     INTERFACES (Abstractions)                                     CONCRETE IMPLEMENTATIONS


  ┌──────────────────────────────────┐          ◄─────── implements ───────   ┌──────────────────────────────────┐
  │          «abstract»              │                                         │           Keyboard               │
  │          InputDevice             │                                         ├──────────────────────────────────┤
  ├──────────────────────────────────┤                                         │  (no attributes)                 │
  │  + input_data()*                 │          ◄─────── implements ───────   ├──────────────────────────────────┤
  └──────────────────────────────────┘                                         │  + input_data()                  │
                                                                               └──────────────────────────────────┘
            ^ has-a
            |                                                                  ┌──────────────────────────────────┐
            |                                   ◄─────── implements ───────   │          TouchScreen             │
  ┌──────────────────────────────────┐                                         ├──────────────────────────────────┤
  │          «abstract»              │           ◄─────── implements ───────   │  (no attributes)                 │
  │          OutputDevice            │                                         ├──────────────────────────────────┤
  ├──────────────────────────────────┤                                         │  + input_data()                  │
  │  + output_data(data)*            │                                         │  + output_data(data)             │
  └──────────────────────────────────┘                                         └──────────────────────────────────┘
                                                 NOTE: TouchScreen implements
            ^ has-a                              BOTH InputDevice & OutputDevice
            |
            |                                                                  ┌──────────────────────────────────┐
  ┌──────────────────────────────────┐                                         │            Monitor               │
  │          «abstract»              │          ◄─────── implements ───────   ├──────────────────────────────────┤
  │          Processor               │                                         │  (no attributes)                 │
  ├──────────────────────────────────┤                                         ├──────────────────────────────────┤
  │  + process_data(data)*           │                                         │  + output_data(data)             │
  └──────────────────────────────────┘                                         └──────────────────────────────────┘
       ^                   ^ has-a
       | has-a             |                                                   ┌──────────────────────────────────┐
       |                   |              ◄─────── implements ───────          │           IntelChip              │
  ┌──────────────────────────────────┐                                         ├──────────────────────────────────┤
  │          «abstract»              │                                         │  (no attributes)                 │
  │          Storage                 │          ◄─────── implements ───────   ├──────────────────────────────────┤
  ├──────────────────────────────────┤                                         │  + process_data(data)            │
  │  + store_data(data)*             │                                         └──────────────────────────────────┘
  │  + retrieve_data()*              │
  └──────────────────────────────────┘                                         ┌──────────────────────────────────┐
                                                ◄─────── implements ───────    │            ARMChip               │
                                                                               ├──────────────────────────────────┤
                                                                               │  (no attributes)                 │
                                                                               ├──────────────────────────────────┤
                                                                               │  + process_data(data)            │
                                                                               └──────────────────────────────────┘

                                                                               ┌──────────────────────────────────┐
                                                ◄─────── implements ───────    │         InternalMemory           │
                                                                               ├──────────────────────────────────┤
                                                                               │  - _memory                       │
                                                                               ├──────────────────────────────────┤
                                                                               │  + store_data(data)              │
                                                                               │  + retrieve_data()               │
                                                                               └──────────────────────────────────┘
```

---

## Relationship Key

```
  ◄─────── implements ───────     Concrete class fulfils an abstract interface
               |
               v                  extends / inherits (subclass --> parent)
              ^ has-a             Computer holds a reference to the abstraction
         *                        Abstract method — must be overridden by subclass
   «abstract»                     Cannot be instantiated directly
   «property»                     Controlled via getter / setter
   - attribute                    Private  (self._name  convention)
   + attribute                    Public
```

---

## SOLID Mapped to the Diagram

```
  ┌─────┬───────────────────────────────────────────────────────────────────────────────────────┐
  │  S  │  Every box has one job. Keyboard only inputs. Monitor only outputs. Computer only      │
  │     │  orchestrates. No class bleeds into another's responsibility.                          │
  ├─────┼───────────────────────────────────────────────────────────────────────────────────────┤
  │  O  │  Adding ARMChip or a new Microphone class requires ZERO changes to Computer.           │
  │     │  Just add a new box that implements the right interface.                               │
  ├─────┼───────────────────────────────────────────────────────────────────────────────────────┤
  │  L  │  DesktopComputer and Laptop both extend Computer without breaking its behaviour.       │
  │     │  Laptop simply omits swap_input_device — it never promises what it cannot deliver.     │
  ├─────┼───────────────────────────────────────────────────────────────────────────────────────┤
  │  I  │  Five small interfaces instead of one fat one. TouchScreen only implements             │
  │     │  InputDevice + OutputDevice. Laptop is never forced to touch Swappable.                │
  ├─────┼───────────────────────────────────────────────────────────────────────────────────────┤
  │  D  │  Computer's has-a arrows all point to ABSTRACTIONS, never to Keyboard or IntelChip.   │
  │     │  Concrete objects are injected from outside — Dependency Injection.                    │
  └─────┴───────────────────────────────────────────────────────────────────────────────────────┘
```