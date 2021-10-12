import asyncio


async def stopwatch():
    count = 0
    while True:
        await asyncio.sleep(1)
        count += 1
        print(count)


async def main():
    task = asyncio.create_task(stopwatch())
    await asyncio.sleep(3)
    task.cancel()


asyncio.run(main())
