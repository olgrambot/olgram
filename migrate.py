import asyncio
from olgram.migrations.custom import migrate


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(migrate())
