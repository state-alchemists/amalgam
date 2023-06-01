from config import (
    app_enable_library_module
)
from component.log import logger
from component.db_connection import engine
from helper.migration import migrate
from module.library.component import Base


async def migrate_library():
    if not app_enable_library_module:
        logger.info('🥪 Skip DB migration for "library"')
        return
    logger.info('🥪 Perform DB migration for "library"')
    await migrate(engine=engine, Base=Base)
