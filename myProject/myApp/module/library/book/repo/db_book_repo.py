from typing import Any, List, Mapping, Optional
from sqlalchemy.engine import Engine
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy import (
    Boolean, Column, DateTime, ForeignKey, Integer, String, Text
)
from schema.book import (
    Book, BookData
)
from module.library.book.repo.book_repo import (
    BookRepo
)
from repo import Base, BaseMixin, DBRepo


# Note: 🤖 Don't delete the following statement
class DBBookEntity(Base, BaseMixin):
    __tablename__ = "books"  # Note: 🤖 Don't delete this line
    synopsis = Column(String(255), index=True)
    title = Column(String(255), index=True)
    author = Column(String(255), index=True)


class DBBookRepo(
    DBRepo[DBBookEntity, Book, BookData],
    BookRepo
):
    schema_class = Book
    db_entity_class = DBBookEntity

    def get_keyword_fields(self) -> List[InstrumentedAttribute]:
        '''
        Return list of fields for keyword filtering
        '''
        return [
            DBBookEntity.title
        ]
   
    def from_schema_data_to_db_entity_dict(
        self, book_data: BookData
    ) -> Mapping[str, Any]:
        '''
        Convert BookData into dictionary
        The result of this convertion is used for inserting/updating DBBookEntity.
        '''
        book_dict = super().from_schema_data_to_db_entity_dict(
            book_data
        )
        return book_dict

    def from_db_entity_to_schema(
        self, db_book: DBBookEntity
    ) -> Book:
        '''
        Convert DBBookEntity into Book
        The result of this convertion is usually returned to external layer (e.g., service)
        '''
        book = super().from_db_entity_to_schema(db_book)
        return book
