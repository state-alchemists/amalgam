from config import APP_ENABLE_LIBRARY_MODULE
from helper.migration import migrate
from integration.db_connection import engine
from integration.log import logger
from module.library.integration import Base


async def migrate_library():
    if not APP_ENABLE_LIBRARY_MODULE:
        logger.info('🥪 Skip DB migration for "library"')
        return
    logger.info('🥪 Perform DB migration for "library"')
    await migrate(engine=engine, Base=Base)
