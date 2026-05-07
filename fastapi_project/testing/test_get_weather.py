from src.http_client import client
import asyncio



async def testing():
    print(await client.get_weather('moscow'))


if __name__ == '__main__':
    asyncio.run(testing())