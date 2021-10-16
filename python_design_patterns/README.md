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
- Builder pattern does not use abstraction, (rely on interfaces) and violates OCP, since the builder is tightly coupled with the implementation of objects it builds (low-level).
- __Builder Facets__ uses a builder [__facade__](code/udemy/builder/builder_facets.py) with high-level methods that return lower-level category builders (aspects), to simplify construction in phases. It also helps to reduce the size of each method.
- Generally to avoid __violation of OCP__ use inheritance with specialized __sub-builders.__ Interesting example of starting with specialization and move up to less specialized builder in one fluent interface pass [code/udemy/builder/builder_inheritance.py](code/udemy/builder/builder_inheritance.py)

### Factory

- __Problem:__ Object creation becomes convoluted.
  - Initializer is not descriptive, always `__init__`
  - Cannot overload with same sets of arguments with different names (you can use only __default keyword arguments__ to overload)
  - The above can turn into __optional parameter hell__
- __Wholesale__ object creation can be __outsourced__ to factories.
  - A separate method usually static, or function (Factory Method) [code/udemy/factory/factory.py](code/udemy/factory/factory.py)
  - Separate class or inner (Factory) [code/udemy/factory/factory.py](code/udemy/factory/factory.py)
  - Hierarchy of factories - provide factories abstraction (improve DIP & OCP) (Abstract Factory) [code/udemy/factory/abstract_factory.py](code/udemy/factory/abstract_factory.py)
    - `HotDrinkMachine` is an interesting implementation using homoiconicity to evaluate `eval()` the name of constructed classes.

### Prototype

- __Problem:__ Complicated objects are designed not from scratch, but from existing products.
  - They reiterate existing designs
- An existing (partially or fully constructed) design is a __Prototype__
- Make a copy (clone) of a prototype and customize it.
  - Requires __deep copy__ support. `import copy; result = copy.deepcopy(proto)` [code/udemy/prototype/prototype.py](code/udemy/prototype/prototype.py)
  - We make cloning convenient (e.g. via a Factory)
- __Streamline__ the process of creation of multiple complex objects, with small customization differences.

### Singleton

- __Problem:__ 