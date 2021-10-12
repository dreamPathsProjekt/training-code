import asyncio


class Stopwatch:
    def __await__(self):
        yield


async def main():
    await Stopwatch()


asyncio.run(main())
