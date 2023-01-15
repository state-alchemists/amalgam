from typing import Optional
from transport import AppMessageBus, AppRPC
from schema.user import User
from schema.activity import ActivityData
from schema.book import (
    Book, BookData, BookResult
)
from module.library.book.repo.book_repo import (
    BookRepo
)
from fastapi import HTTPException


class BookService():
    '''
    Service to handle book
    '''

    def __init__(
        self,
        mb: AppMessageBus,
        rpc: AppRPC,
        book_repo: BookRepo
    ):
        '''
        Init Book service.
        '''
        self.mb = mb
        self.rpc = rpc
        self.book_repo = book_repo

    def find(
        self,
        keyword: str,
        limit: int,
        offset: int,
        current_user: Optional[User] = None
    ) -> BookResult:
        '''
        Find books
        '''
        count = self.book_repo.count(keyword)
        rows = [
            self._fulfill_book(row)
            for row in self.book_repo.find(
                keyword, limit, offset
            )
        ]
        return BookResult(count=count, rows=rows)

    def find_by_id(
        self,
        id: str,
        current_user: Optional[User] = None
    ) -> Optional[Book]:
        '''
        Find book
        '''
        book = self._find_book_by_id_or_error(
            id, current_user
        )
        book = self._fulfill_book(
            book
        )
        return book

    def insert(
        self,
        book_data: BookData,
        current_user: User
    ) -> Optional[Book]:
        '''
        Insert book
        '''
        book_data.created_by = current_user.id
        book_data.updated_by = current_user.id
        book_data = self._validate_book_data(
            book_data
        )
        new_book = self.book_repo.insert(
            book_data
        )
        self.mb.publish_activity(ActivityData(
            user_id=current_user.id,
            activity='insert',
            object='book',
            row=new_book.dict(),
            row_id=new_book.id
        ))
        new_book = self._fulfill_book(
            new_book
        )
        return new_book

    def update(
        self,
        id: str,
        book_data: BookData,
        current_user: User
    ) -> Optional[Book]:
        '''
        Update book
        '''
        self._find_book_by_id_or_error(id, current_user)
        book_data.updated_by = current_user.id
        book_data = self._validate_book_data(
            book_data, id
        )
        updated_book = self.book_repo.update(
            id,
            book_data
        )
        self.mb.publish_activity(ActivityData(
            user_id=current_user.id,
            activity='update',
            object='book',
            row=updated_book.dict(),
            row_id=updated_book.id
        ))
        updated_book = self._fulfill_book(
            updated_book
        )
        return updated_book

    def delete(
        self,
        id: str,
        current_user: User
    ) -> Optional[Book]:
        '''
        Delete book
        '''
        self._find_book_by_id_or_error(id, current_user)
        deleted_book = self.book_repo.delete(
            id
        )
        self.mb.publish_activity(ActivityData(
            user_id=current_user.id,
            activity='delete',
            object='book',
            row=deleted_book.dict(),
            row_id=deleted_book.id
        ))
        deleted_book = self._fulfill_book(
            deleted_book
        )
        return deleted_book

    def _find_book_by_id_or_error(
        self,
        id: Optional[str] = None,
        current_user: Optional[User] = None
    ) -> Optional[Book]:
        '''
        Find book or throw an error if not found
        '''
        book = self.book_repo.find_by_id(id)
        if book is None:
            raise HTTPException(
                status_code=404,
                detail='book id not found: {}'.format(id)
            )
        return book

    def _fulfill_book(
        self,
        book: Book
    ) -> Book:
        '''
        Complete book.
        You can use this method to add default fields etc.
        '''
        return book

    def _validate_book_data(
        self,
        book_data: BookData,
        id: Optional[str] = None
    ) -> BookData:
        '''
        Validate book_data.
        You can throw HTTPException when the data is not right
        '''
        return book_data
