from typing import Optional
from schemas.book import Book, BookData, BookResult
from repos.book import BookRepo

class BookService():

    def __init__(self, book_repo: BookRepo):
        self.book_repo = book_repo

    def find(self, keyword: str, limit: int, offset: int) -> BookResult:
        count = self.book_repo.count(keyword)
        rows = self.book_repo.find(keyword, limit, offset)
        return BookResult(count=count, rows=rows)

    def find_by_id(self, id: str) -> Optional[Book]:
        return self.book_repo.find_by_id(id)

    def insert(self, book_data: BookData) -> Optional[Book]:
        return self.book_repo.insert(book_data)

    def update(self, id: str, book_data: BookData) -> Optional[Book]:
        return self.book_repo.update(id, book_data)

    def delete(self, id: str) -> Optional[Book]:
        return self.book_repo.delete(id)