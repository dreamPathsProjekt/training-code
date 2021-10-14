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

Gamma Categorization:

- Creational - Deal with creation of objects
  - Explicit (constructor) or implicit (DI framework, reflection etc.)
  - Wholesale (single statements) or piecewise (sevaral statements) creation
- Structural - Concerned with the structures of classes, objects (e.g. class members)
  - Many patterns are wrappers that mimic the underlying class' interface
  - Stress the important of good API design with convenience in usability
- Behavioral - all different, no central theme, solve particular problems

Principles:

- SRP
- OCP - Interesting implementation using `__and__` & duck-typing polymorphism: [ocp.py](code/udemy/SOLID/ocp.py)
  - In Python we cannot overload the `and` operator, but by using protocols (implement `__and__` method) we can overload the binary `AND` operator `&` to accept non-binary objects.
- LSP
- ISP - Interesting implementation using `ABC` and __multiple inheritance__ of smaller, multiple interfaces [isp.py](code/udemy/SOLID/isp.py)
- DIP

### Builder

- __Problem:__ Some objects require a lot of ceremony to create
  - Having an object with 10 initializer arguments, not productive.
  - __Piecewise Construction__ - Provide an API for object construction step by step.
  - Most usually, usage of __fluent interfaces__ - object methods that return the object and can be chained together.

