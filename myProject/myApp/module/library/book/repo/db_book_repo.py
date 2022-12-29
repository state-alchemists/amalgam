from typing import List, Optional
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from schema.book import Book, BookData
from module.library.book.repo.book_repo import BookRepo
from repo import Base

import uuid
import datetime

# Note: 🤖 Don't delete the following line; Zaruba uses it for pattern matching
class DBBookEntity(Base):
    __tablename__ = "books"
    id = Column(String(36), primary_key=True, index=True)
    title = Column(String(255), index=True)
    author = Column(String(255), index=True)
    synopsis = Column(String(255), index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow) # Note: 🤖 Don't delete this line; Zaruba uses it for pattern matching
    created_by = Column(String(36), nullable=True)
    updated_at = Column(DateTime, nullable=True)
    updated_by = Column(String(36), nullable=True)


# Note: 🤖 Don't delete the following line; Zaruba uses it for pattern matching
class DBBookRepo(BookRepo):

    def __init__(self, engine: Engine, create_all: bool):
        self.engine = engine
        if create_all:
            Base.metadata.create_all(bind=engine)


    def find_by_id(self, id: str) -> Optional[Book]:
        db = Session(self.engine, expire_on_commit=False)
        book: Book
        try:
            db_book = db.query(DBBookEntity).filter(DBBookEntity.id == id).first()
            if db_book is None:
                return None
            book = Book.from_orm(db_book)
        finally:
            db.close()
        return book


    def find(self, keyword: str, limit: int, offset: int) -> List[Book]:
        db = Session(self.engine, expire_on_commit=False)
        books: List[Book] = []
        try:
            keyword_filter = self._get_keyword_filter(keyword)
            db_books = db.query(DBBookEntity).filter(DBBookEntity.title.like(keyword_filter)).offset(offset).limit(limit).all()
            books = [Book.from_orm(db_result) for db_result in db_books]
        finally:
            db.close()
        return books


    def count(self, keyword: str) -> int:
        db = Session(self.engine, expire_on_commit=False)
        book_count = 0
        try:
            keyword_filter = self._get_keyword_filter(keyword)
            book_count = db.query(DBBookEntity).filter(DBBookEntity.title.like(keyword_filter)).count()
        finally:
            db.close()
        return book_count


    # Note: 🤖 Don't delete the following line; Zaruba uses it for pattern matching
    def insert(self, book_data: BookData) -> Optional[Book]:
        db = Session(self.engine, expire_on_commit=False)
        book: Book
        try:
            new_book_id = str(uuid.uuid4())
            db_book = DBBookEntity(
                id=new_book_id,
                title=book_data.title,
                author=book_data.author,
                synopsis=book_data.synopsis,
                created_at=datetime.datetime.utcnow(), # Note: 🤖 Don't delete this line; Zaruba uses it for pattern matching
                created_by=book_data.created_by,
                updated_at=datetime.datetime.utcnow(),
                updated_by=book_data.updated_by,
            )
            db.add(db_book)
            db.commit()
            db.refresh(db_book) 
            book = Book.from_orm(db_book)
        finally:
            db.close()
        return book


    # Note: 🤖 Don't delete the following line; Zaruba uses it for pattern matching
    def update(self, id: str, book_data: BookData) -> Optional[Book]:
        db = Session(self.engine, expire_on_commit=False)
        book: Book
        try:
            db_book = db.query(DBBookEntity).filter(DBBookEntity.id == id).first()
            if db_book is None:
                return None
            db_book.title = book_data.title
            db_book.author = book_data.author
            db_book.synopsis = book_data.synopsis
            db_book.updated_at = datetime.datetime.utcnow() # Note: 🤖 Don't delete this line; Zaruba uses it for pattern matching
            db_book.updated_by = book_data.updated_by
            db.add(db_book)
            db.commit()
            db.refresh(db_book) 
            book = Book.from_orm(db_book)
        finally:
            db.close()
        return book


    def delete(self, id: str) -> Optional[Book]:
        db = Session(self.engine, expire_on_commit=False)
        book: Book
        try:
            db_book = db.query(DBBookEntity).filter(DBBookEntity.id == id).first()
            if db_book is None:
                return None
            db.delete(db_book)
            db.commit()
            book = Book.from_orm(db_book)
        finally:
            db.close()
        return book


    def _get_keyword_filter(self, keyword: str) -> str:
        return '%{}%'.format(keyword) if keyword != '' else '%'
