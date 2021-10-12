# Asynchronous Python With Asyncio

- [https://www.udemy.com/course/asynchronous-python-with-asyncio](https://www.udemy.com/course/asynchronous-python-with-asyncio)
- `asyncio` api got a renovation on __Python 3.7__

## What, Why & Threads vs Asyncio

Most usual Blocking Calls:

- HTTP Requests
- Database connections, queries
- Writing to log files

Why use asyncio (with __event loop__ at its core)

- Alternative to __multithreading__ -> hard to debug/troubleshooting
- Allows to use many more network connections (e.g. websockets)

### Threading vs Asyncio

- Threading runs on __multiple__ CPU threads, asyncio runs (or can run) on __one cpu thread.__
- Complexity of code is higher on asyncio vs multithreading
- Harder to debug / reason in multithreading (e.g. shared memory, race conditions, deadlocks)

## Basics of `async` and `await`

### Asynchronous functions

```Python
import asyncio

async def main():
    print('hello...')
    await asyncio.sleep(2)
    print('...world')

# Cannot run async function like this
main()
# Traceback RuntimeWarning: coroutine 'main' was never awaited
#   main()
# RuntimeWarning: Enable tracemalloc to get the object allocation traceback

# Running async function
asyncio.run(main())

# The result of an async function, is a coroutine object
result = main()
<coroutine object main at 0x7f503fc923c0>

# Try to use send method of coroutine (behind the scenes of asyncio.run)
result = main()

try:
    result.send(None)
except StopIteration as se:
    print(se)
# Runs with RuntimeError: no running event loop
# Will run successfully if no awaitable is inside function
```

### Asynchronous Iterators

- [Iterable vs Iterator protocols](https://stackoverflow.com/questions/9884132/what-exactly-are-iterator-iterable-and-iteration)

```Python
import asyncio
import random


class EggBoiler:
    def __init__(self, amount):
        self.eggs = iter(range(1, amount + 1))

    # Asynchronous iterable protocol, similar to __iter__ on iterable
    # An iterable is an object that you can get an iterator from, using iter() built-in method.
    # Here the async iterable just returns itseld (async iterator that implements the __anext__ method)
    def __aiter__(self):
        return self

    # Asynchronous iterator protocol, similar to __next__ on iterator.
    async def __anext__(self):
        try:
            egg = next(self.eggs)
        except StopIteration:
            # StopIteration raise for async
            raise StopAsyncIteration
        # Important: Returns async method
        return self.boil(egg)

    async def boil(self, egg):
        await asyncio.sleep(random.randint(2, 5))
        print(f'Egg #{egg} is boiling')


# await egg produces a synchronous experience, wait one egg each iteration
async def main():
    async for egg in EggBoiler(4):
        await egg

# Improve performance, boil eggs more than 1 at a time
async def main():
    eggs = []
    async for egg in EggBoiler(4)
        eggs.append(egg)
    # Aggregate results from the coroutines, wrap them in futures.
    # All results share the same eventloop.
    await asyncio.gather(*eggs)

asyncio.run(main())

```

### The `@asynccontextmanager` Decorator

```Python
import asyncio
from contextlib import asynccontextmanager


@asynccontextmanager
async def connection():
    print('Setting up connection')
    # asyncio.sleep is awaitable
    await asyncio.sleep(1)
    yield {'driver': 'sqlite'}
    await asyncio.sleep(1)
    print('Shutting down')


async def main():
    async with connection() as db:
        print(db, 'is ready')

asyncio.run(main())
```

### Context Manager Classes

```Python
import asyncio

# Context manager protocol - async version
# Both methods need to return an awaitable (any function with async in front returns an awaitable - return type: -> Coroutine)
class Connection:
    # Equivalent of sync __enter__
    async def __aenter__(self):
        print('Setting up a connection')
        await asyncio.sleep(1)
        return {'driver': 'sqlite'}

    # Equivalent of sync __exit__
    async def __aexit__(self, exc_type, exc, tb):
        await asyncio.sleep(1)
        print('Connection is closed')


async def main():
    async with Connection() as db:
        print(db, 'is ready')

asyncio.run(main())
```

### Asynchronous Generators

```Python
import asyncio

# Async generator - return type: -> AsyncGenerator
# Without the yield it would be a simple Coroutine
async def download(urls):
    for url in urls:
        await asyncio.sleep(1)
        response = {'status': 200, 'data': f'content of {url}'}
        yield response


async def main():
    urls = [
        'google.com',
        'bing.com',
        'duckduckgo.com',
    ]

    # Similar to async iteration
    async for value in download(urls):
        print(value)

asyncio.run(main())
```

### Asynchronous List Comprehension

```Python
# Continue from previous example - use comprehension to run through async generator

async def handle(err_response):
    print('logging error response for', err_response)

async def main():
    urls = [
        'google.com',
        'bing.com',
        'duckduckgo.com',
    ]

    # Similar to async iteration
    errors = [r async for r in download(urls) if r['status'] != 200]
    print(errors)

    # Use Await in comprehension
    [await handle(e) for e in errors]
```

## Coroutines & Awaitables

```Python
# Module to help with object reflection
import inspect

# Calling an async function returns (coroutinefunction) a Coroutine (awaitable)
async def main():
    pass


print(type(main))
print(inspect.iscoroutinefunction(main))
print(type(main()))
print(dir(main()))

<class 'function'>
# Difference vs simple function using inspect.iscoroutinefunction(main)
True
# Return type
<class 'coroutine'>
# Reflection on coroutine, characteristic methods: close, cr_ family, send, throw
# send is used to manually invoke the coroutine
# throw is used to inject exceptions in coroutines
['__await__', '__class__', '__del__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__name__', '__ne__', '__new__', '__qualname__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'close', 'cr_await', 'cr_code', 'cr_frame', 'cr_origin', 'cr_running', 'send', 'throw']
```

### Ways to run & cancel coroutines

```Python
# Ways to run coroutines
# 1. using asyncio - usually to run main
asyncio.run(main())
# 2. await keyword
await download()
# 3. create_task
asyncio.create_task(log())

# Cancel coroutines (without cancel tasks)
async def stopwatch():
    count = 0
    while True:
        await asyncio.sleep(1)
        count += 1
        print(count)

async def main():
    # Manually start using send
    coro = stopwatch()
    coro.send(None)
    await asyncio.sleep(2)
    # Cancel with Exception injection using throw
    coro.throw(asyncio.CancelledError)

# The above methods should not be used by calls, but from other higher level functions/methods, such in the case of tasks and asyncio.run()
async def main():
    # Proper way to invoke
    task = asyncio.create_task(stopwatch())
    await asyncio.sleep(2)
    # Proper way to cancel
    task.cancel()

# send & throw are low-level coroutine methods (not dunder but follow same philosophy)
# They are used by high-level asyncio.create_task() & task.cancel()
```

### Types of Awaitable Objects

The `await` expression only works with awaitables:

- A `Coroutine`
- A `Task`
- A `Future`
- A __custom awaitable__ by implementing the `__await__` method, that needs to return an __iterable.__

```Python
class Stopwatch():
    # Note: __await__ is not async, just standard method
    def __await__(self):
        # Not very useful example (does nothing), but yield returns a generator (iterable)
        yield


async def main():
    # Created a custome awaitable
    await Stopwatch()

asyncio.run(main())
```

## Tasks, Futures & interacting with the Event Loop (low-level API)

### Task Objects

```Python
# Tasks are the main way to run coroutines in the event loop

async def main():
    task = asyncio.create_task(stopwatch())
    print(task)
    # Task contains name: get_name, set_name methods, fields _coro: coroutine to run, _state (pending)
    # <Task pending name='Task-2' coro=<stopwatch() running at /home/dreampaths/Documents/training-code/async_python/code/4_tasks_futures/main_4_2.py:4>>

    # Reflect Task object - some task methods might be missing in versions: 3.7 < version < 3.8
    print(dir(task))
    ['__await__', '__class__', '__class_getitem__', '__del__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '_asyncio_future_blocking', '_callbacks', '_cancel_message', '_coro', '_exception', '_fut_waiter', '_log_destroy_pending', '_log_traceback', '_loop', '_make_cancelled_error', '_must_cancel', '_repr_info', '_result', '_source_traceback', '_state', 'add_done_callback', 'cancel', 'cancelled', 'done', 'exception', 'get_coro', 'get_loop', 'get_name', 'get_stack', 'print_stack', 'remove_done_callback', 'result', 'set_exception', 'set_name', 'set_result']

def callb(task):
    # Callback should take task as only argument. Otherwise:
    # TypeError: callb() takes 0 positional arguments but 1 was given
    # Similar flow to a decorator
    print('task is done', task)


async def main():
    task = asyncio.create_task(stopwatch())
    # Callback to run on done.
    task.add_done_callback(callb)
    await task

# 1
# 2
# 3
# 4
# task is done <Task finished name='Task-2' coro=<stopwatch() done, defined at /home/dreampaths/Documents/training-code/async_python/code/4_tasks_futures/main_4_2.py:4> result=None>
# Task on done contains a result object, we can retrieve or set it.
```

### Interact with the Event Loop

```Python
# Event loop is only accessible inside the context of a coroutine
# Throws Runtime Error - since no event loop running
print(asyncio.get_running_loop())

async def main():
    print(asyncio.get_running_loop())
    # <_UnixSelectorEventLoop running=True closed=False debug=False>
    # As long as the code is running on single thread, this object is a singleton.
    # Each OS thread is running its own event loop.
    task = asyncio.create_task(stopwatch())
    task.add_done_callback(callb)
    await task

asyncio.run(main())
```

### Futures

```Python
# A Task is subclass of Future - another awaitable object
# A lot of the methods found on Task are also available on Future
async def main():
    task = asyncio.create_task(stopwatch())
    task.add_done_callback(callb)
    # Subclass of Future - returns True
    print(asyncio.isfuture(task))
    await task
```

[What is the difference between futures and tasks?](https://stackoverflow.com/questions/64851715/python-asyncio-future-vs-task)

- In short, __future__ is the more general concept of a __container of an async result__, akin to a JavaScript __promise__.
- Task is a subclass of future specialized for __executing coroutines__.
