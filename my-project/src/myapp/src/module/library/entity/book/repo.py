from sqlalchemy import Column, String
from core.repo import Repo, DBEntityMixin, DBRepo
from module.library.schema.book import (
    Book, BookData
)
from module.library.component import Base


class DBEntityBook(Base, DBEntityMixin):
    __tablename__ = "books"
    code = Column(String)
    title: Column = Column(String)


class BookRepo(Repo[Book, BookData]):
    pass


class BookDBRepo(
    DBRepo[Book, BookData], BookRepo
):
    schema_cls = Book
    db_entity_cls = DBEntityBook
