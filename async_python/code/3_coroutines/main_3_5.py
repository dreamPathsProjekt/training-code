import asyncio


class Stopwatch:
    async def __await__(self):
        yield


async def main():
    await Stopwatch()


asyncio.run(main())
