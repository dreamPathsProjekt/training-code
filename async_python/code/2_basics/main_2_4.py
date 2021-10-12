import asyncio
from contextlib import asynccontextmanager


@asynccontextmanager
async def connection():
    print('Setting up connection')
    await asyncio.sleep(1)
    yield {'driver': 'sqlite'}
    await asyncio.sleep(1)
    print('Shutting down')


async def main():
    async with connection() as db:
        print(db, 'is ready')

asyncio.run(main())
