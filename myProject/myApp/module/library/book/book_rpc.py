from typing import Any, Optional, Mapping
from core import AuthService
from transport import AppMessageBus, AppRPC
from schema.book import (
    Book, BookData
)
from schema.user import User
from module.library.book.book_service import (
    BookService
)

import logging


def register_book_rpc(mb: AppMessageBus, rpc: AppRPC, auth_service: AuthService, book_service: BookService):

    @rpc.handle('find_book')
    def find_books(
        keyword: str,
        limit: int,
        offset: int,
        current_user_data: Optional[Mapping[str, Any]]
    ) -> Mapping[str, Any]:
        current_user = _get_user_from_dict(current_user_data)
        book_result = book_service.find(
            keyword, limit, offset, current_user
        )
        return book_result.dict()

    @rpc.handle('find_book_by_id')
    def find_book_by_id(
        id: str,
        current_user_data: Optional[Mapping[str, Any]]
    ) -> Optional[Mapping[str, Any]]:
        current_user = _get_user_from_dict(current_user_data)
        book = book_service.find_by_id(
            id, current_user
        )
        return _book_as_dict(book)

    @rpc.handle('insert_book')
    def insert_book(
        book_data: Mapping[str, Any],
        current_user_data: Mapping[str, Any]
    ) -> Optional[Mapping[str, Any]]:
        current_user = User.parse_obj(current_user_data)
        book = BookData.parse_obj(
            book_data)
        new_book = book_service.insert(
            book, current_user
        )
        return _book_as_dict(new_book)

    @rpc.handle('update_book')
    def update_book(
        id: str,
        book_data: Mapping[str, Any],
        current_user_data: Mapping[str, Any]
    ) -> Optional[Mapping[str, Any]]:
        current_user = User.parse_obj(current_user_data)
        book = BookData.parse_obj(
            book_data)
        book.updated_by = current_user.id
        updated_book = book_service.update(
            id, book, current_user
        )
        return _book_as_dict(updated_book)

    @rpc.handle('delete_book')
    def delete_book(
        id: str,
        current_user_data: Mapping[str, Any]
    ) -> Optional[Mapping[str, Any]]:
        current_user = User.parse_obj(current_user_data)
        deleted_book = book_service.delete(
            id, current_user
        )
        return _book_as_dict(deleted_book)

    def _get_user_from_dict(
        user_data: Optional[Mapping[str, Any]]
    ) -> Optional[User]:
        if user_data is None:
            return None
        return User.parse_obj(user_data)

    def _book_as_dict(
        book: Optional[Book]
    ) -> Optional[Mapping[str, Any]]:
        if book is None:
            return None
        return book.dict()

    logging.info('Register library.book RPC handler')
