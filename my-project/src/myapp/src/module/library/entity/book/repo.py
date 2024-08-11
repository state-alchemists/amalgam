from component.repo import DBEntityMixin, DBRepo, Repo
from module.library.integration import Base
from module.library.schema.book import (
    Book,
    BookData,
)
from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Double,
    Float,
    Integer,
    String,
    Text,
    Time,
)


class DBEntityBook(Base, DBEntityMixin):
    class Config:
        from_attributes = True

    __tablename__ = "books"
    code = Column(String)
    title: Column = Column(String)
    page_number: Column = Column(Integer)
    purchase_date: Column = Column(Date)
    available: Column = Column(Boolean)
    synopsis: Column = Column(Text)


class BookRepo(Repo[Book, BookData]):
    pass


class BookDBRepo(
    DBRepo[Book, BookData], BookRepo
):
    schema_cls = Book
    db_entity_cls = DBEntityBook
