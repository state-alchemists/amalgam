from component.db_connection import engine
from component.log import logger
from module.library.entity.book.repo import (
    BookDBRepo,
    BookRepo,
)

book_repo: BookRepo = BookDBRepo(
    logger=logger, engine=engine
)
