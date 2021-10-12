import asyncio


class Connection:
    async def __aenter__(self):
        print('Setting up a connection')
        await asyncio.sleep(1)
        return {'driver': 'sqlite'}

    async def __aexit__(self, exc_type, exc, tb):
        await asyncio.sleep(1)
        print('Connection is closed')


async def main():
    async with Connection() as db:
        print(db, 'is ready')

asyncio.run(main())
