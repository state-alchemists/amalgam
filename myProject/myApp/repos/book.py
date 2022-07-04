from typing import List, Mapping, Optional
from schemas.book import Book, BookData

import abc
import json
import uuid
import datetime

class BookRepo(abc.ABC):

    @abc.abstractmethod
    def find_by_id(self, id: str) -> Optional[Book]:
        pass

    @abc.abstractmethod
    def find(self, keyword: str, limit: int, offset: int) -> List[Book]:
        pass

    @abc.abstractmethod
    def count(self, keyword: str) -> int:
        pass

    @abc.abstractmethod
    def insert(self, book_data: BookData) -> Optional[Book]:
        pass

    @abc.abstractmethod
    def update(self, id: str, book_data: BookData) -> Optional[Book]:
        pass

    @abc.abstractmethod
    def delete(self, id: str) -> Optional[Book]:
        pass


class MemBookRepo(BookRepo):

    def __init__(self):
        self._book_map: Mapping[str, Book] = {}

    def set_storage(self, book_map: Mapping[str, Book]):
        self._book_map = book_map

    def find_by_id(self, id: str) -> Optional[Book]:
        if id not in self._book_map:
            return None
        return self._book_map[id]

    def find(self, keyword: str, limit: int, offset: int) -> List[Book]:
        mem_books = list(self._book_map.values())
        books: List[Book] = []
        for index in range(offset, limit+offset):
            if index >= len(mem_books):
                break
            mem_book = mem_books[index]
            books.append(mem_book)
        return books

    def count(self, keyword: str) -> List[Book]:
        mem_books = list(self._book_map.values())
        return len(mem_books)

    def insert(self, book_data: BookData) -> Optional[Book]:
        if id not in self._book_map:
            return None
        new_book_id = str(uuid.uuid4())
        new_book = Book(
            id=new_book_id,
            title=book_data.title,
            author=book_data.author,
            synopsis=book_data.synopsis,
            created_at=datetime.datetime.utcnow(),
            created_by=book_data.created_by
        )
        self._book_map[new_book_id] = new_book
        return new_book

    def update(self, id: str, book_data: BookData) -> Optional[Book]:
        if id not in self._book_map:
            return None
        mem_book = self._book_map[id]
        mem_book.title = book_data.title
        mem_book.author = book_data.author
        mem_book.synopsis = book_data.synopsis
        mem_book.updated_at = datetime.datetime.utcnow()
        mem_book.updated_by = book_data.updated_by
        self._book_map[id] = mem_book
        return mem_book

    def delete(self, id: str) -> Optional[Book]:
        if id not in self._book_map:
            return None
        mem_book = self._book_map.pop(id)
        return mem_book