from typing import Optional
from transport import AppMessageBus, AppRPC
from schemas.user import User
from schemas.activity import ActivityData
from schemas.book import Book, BookData, BookResult
from modules.library.book.repos.bookRepo import BookRepo
from fastapi import HTTPException

class BookService():

    def __init__(self, mb: AppMessageBus, rpc: AppRPC, book_repo: BookRepo):
        self.mb = mb
        self.rpc = rpc
        self.book_repo = book_repo


    def find(self, keyword: str, limit: int, offset: int, current_user: Optional[User] = None) -> BookResult:
        count = self.book_repo.count(keyword)
        rows = self.book_repo.find(keyword, limit, offset)
        return BookResult(count=count, rows=rows)


    def find_by_id(self, id: str, current_user: Optional[User] = None) -> Optional[Book]:
        book = self._find_by_id_or_error(id, current_user)
        return book


    def insert(self, book_data: BookData, current_user: User) -> Optional[Book]:
        book_data.created_by = current_user.id
        book_data.updated_by = current_user.id
        book_data = self._validate_data(book_data)
        new_book = self.book_repo.insert(book_data)
        self.mb.publish_activity(ActivityData(
            user_id = current_user.id,
            activity = 'insert',
            object = 'book',
            row = new_book.dict(),
            row_id = new_book.id
        ))
        return new_book


    def update(self, id: str, book_data: BookData, current_user: User) -> Optional[Book]:
        self._find_by_id_or_error(id, current_user)
        book_data.updated_by = current_user.id
        book_data = self._validate_data(book_data, id)
        updated_book = self.book_repo.update(id, book_data)
        self.mb.publish_activity(ActivityData(
            user_id = current_user.id,
            activity = 'update',
            object = 'book',
            row = updated_book.dict(),
            row_id = updated_book.id
        ))
        return updated_book


    def delete(self, id: str, current_user: User) -> Optional[Book]:
        self._find_by_id_or_error(id, current_user)
        deleted_book = self.book_repo.delete(id)
        self.mb.publish_activity(ActivityData(
            user_id = current_user.id,
            activity = 'delete',
            object = 'book',
            row = deleted_book.dict(),
            row_id = deleted_book.id
        ))
        return deleted_book


    def _find_by_id_or_error(self, id: Optional[str] = None, current_user: Optional[User] = None) -> Optional[Book]:
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
