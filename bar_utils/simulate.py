from locate import locatePerc
import asyncio

async def simulate():
    for i in range(101):
        res = await locatePerc(i/100)
        print(res,i)

asyncio.run(simulate())