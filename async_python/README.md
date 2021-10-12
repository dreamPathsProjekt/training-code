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
