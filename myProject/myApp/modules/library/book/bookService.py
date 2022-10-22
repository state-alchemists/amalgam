from typing import Optional
from helpers.transport import RPC, MessageBus
from schemas.user import User
from schemas.book import Book, BookData, BookResult
from modules.library.book.repos.bookRepo import BookRepo
from fastapi import HTTPException

class BookService():

    def __init__(self, mb: MessageBus, rpc: RPC, book_repo: BookRepo):
        self.mb = mb
        self.rpc = rpc
        self.book_repo = book_repo


    def find(self, keyword: str, limit: int, offset: int, current_user: Optional[User] = None) -> BookResult:
        count = self.book_repo.count(keyword)
        rows = self.book_repo.find(keyword, limit, offset)
        return BookResult(count=count, rows=rows)


    def find_by_id(self, id: str, current_user: Optional[User] = None) -> Optional[Book]:
        book = self._find_by_id_or_error(id)
        return book


    def insert(self, book_data: BookData, current_user: User) -> Optional[Book]:
        book_data.created_by = current_user.id
        book_data.updated_by = current_user.id
        book_data = self._validate_data(book_data)
        return self.book_repo.insert(book_data)


    def update(self, id: str, book_data: BookData, current_user: User) -> Optional[Book]:
        self._find_by_id_or_error(id)
        book_data.updated_by = current_user.id
        book_data = self._validate_data(book_data, id)
        return self.book_repo.update(id, book_data)


    def delete(self, id: str, current_user: User) -> Optional[Book]:
        self._find_by_id_or_error(id)
        return self.book_repo.delete(id)


    def _find_by_id_or_error(self, id: Optional[str] = None) -> Optional[Book]:
        book = self.book_repo.find_by_id(id)
        if book is None:
            raise HTTPException(
                status_code=404, 
                detail='Book id not found: {}'.format(id)
            )
        return book


    def _validate_data(self, book_data: BookData, id: Optional[str] = None) -> BookData:
        # TODO: add your custom logic
        # Example: checking duplication
        # if book_data.some_field is not None:
        #     user = self.user_repo.find_by_some_field(book_data.some_field)
        #     if user is not None and (id is None or user.id != id):
        #         raise HTTPException(
        #             status_code=422, 
        #             detail='some_field already exist: {}'.format(book_data.some_field)
        #         )
        return book_data
