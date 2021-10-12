import asyncio
import inspect


async def main():
    pass


print(type(main))
print(inspect.iscoroutinefunction(main))
print(type(main()))
print(dir(main()))
