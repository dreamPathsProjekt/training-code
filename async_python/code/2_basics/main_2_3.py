import asyncio
import random


class EggBoiler:
    def __init__(self, amount):
        self.eggs = iter(range(1, amount + 1))

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            egg = next(self.eggs)
        except StopIteration:
            raise StopAsyncIteration
        return self.boil(egg)

    async def boil(self, egg):
        await asyncio.sleep(random.randint(2, 5))
        print(f'Egg #{egg} is boiling')


async def main():
    eggs = []
    async for egg in EggBoiler(4):
        eggs.append(egg)
    print('We wait for the eggs to boil...')
    await asyncio.gather(*eggs)

asyncio.run(main())
