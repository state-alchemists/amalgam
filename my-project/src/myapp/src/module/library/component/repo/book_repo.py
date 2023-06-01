from component.log import logger
from component.db_connection import engine
from module.library.entity.book.repo import (
    BookRepo, BookDBRepo
)

book_repo: BookRepo = BookDBRepo(
    logger=logger, engine=engine
)
