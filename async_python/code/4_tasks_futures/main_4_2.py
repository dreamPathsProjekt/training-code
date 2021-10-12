import asyncio


async def stopwatch():
    count = 0
    while count < 4:
        await asyncio.sleep(1)
        count += 1
        print(count)


def callb(task):
    print('task is done', task)


async def main():
    task = asyncio.create_task(stopwatch())
    task.add_done_callback(callb)

    await task


asyncio.run(main())
