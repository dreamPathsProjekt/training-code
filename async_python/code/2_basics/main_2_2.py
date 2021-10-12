import asyncio


async def main():
    print('hello...')
    await asyncio.sleep(2)
    print('...world')

asyncio.run(main())
