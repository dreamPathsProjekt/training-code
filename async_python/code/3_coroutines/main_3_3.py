import asyncio


async def download():
    print('dowload document')


async def log():
    print('log to file')


async def main():
    print('in the main function')

    # 2. using await
    await download()

    # 3. create_task
    asyncio.create_task(log())


# 1. using asyncio
asyncio.run(main())
