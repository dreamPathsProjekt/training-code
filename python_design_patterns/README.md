# Python design patterns

## YT Course

### Python Dependency Inversion & Injection

- [Original Video](https://www.youtube.com/watch?v=2ejbLVkCndI)
- [Avoid coverage to try include abstract methods](code/youtube/.coveragerc)

### Factory pattern

- [Factory](https://www.youtube.com/watch?v=s_4ZrtQs8Do)

## Udemy Course

- [https://www.udemy.com/course/design-patterns-python](https://www.udemy.com/course/design-patterns-python)

### SOLID Principles

- Creational
- Structural
- Behavioral

Principles:

- SRP
- OCP - Interesting implementation using `__and__` & duck-typing polymorphism: [ocp.py](code/udemy/SOLID/ocp.py)
  - In Python we cannot overload the `and` operator, but by using protocols (implement `__and__` method) we can overload the binary `AND` operator `&` to accept non-binary objects.
- LSP
- ISP - Interesting implementation using `ABC` and __multiple inheritance__ of smaller, multiple interfaces [isp.py](code/udemy/SOLID/isp.py)
- DIP
