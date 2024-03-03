from component.repo import DBEntityMixin, DBRepo, Repo
from module.library.integration import Base
from module.library.schema.book import (
    Book,
    BookData,
)
from sqlalchemy import Column, String


class DBEntityBook(Base, DBEntityMixin):
    class Config:
        orm_mode = True
        from_attributes = True

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
