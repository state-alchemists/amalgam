import asyncio

from module.auth.migrate import migrate_auth
from module.log.migrate import migrate_log
from module.library.migrate import migrate_library


async def migrate():
    await migrate_auth()
    await migrate_log()
    await migrate_library()


if __name__ == "__main__":
    asyncio.run(migrate())
