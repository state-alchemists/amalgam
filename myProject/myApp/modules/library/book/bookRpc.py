from typing import Any, Optional, Mapping
from core import AuthService
from helpers.transport import RPC, MessageBus
from schemas.book import Book, BookData
from schemas.user import User
from modules.library.book.bookService import BookService

import sys

def register_book_rpc(mb: MessageBus, rpc: RPC, auth_service: AuthService, book_service: BookService):

    @rpc.handle('find_book')
    def find_books(keyword: str, limit: int, offset: int, current_user_data: Optional[Mapping[str, Any]]) -> Mapping[str, Any]:
        current_user = None if current_user_data is None else User.parse_obj(current_user_data)
        book_result = book_service.find(keyword, limit, offset, current_user)
        return book_result.dict()


    @rpc.handle('find_book_by_id')
    def find_book_by_id(id: str, current_user_data: Optional[Mapping[str, Any]]) -> Optional[Mapping[str, Any]]:
        current_user = None if current_user_data is None else User.parse_obj(current_user_data)
        book = book_service.find_by_id(id, current_user)
        return None if book is None else book.dict()


    @rpc.handle('insert_book')
    def insert_book(book_data: Mapping[str, Any], current_user_data: Mapping[str, Any]) -> Optional[Mapping[str, Any]]:
        current_user = User.parse_obj(current_user_data)
        book = BookData.parse_obj(book_data) 
        new_book = book_service.insert(book, current_user)
        return None if new_book is None else new_book.dict()


    @rpc.handle('update_book')
    def update_book(id: str, book_data: Mapping[str, Any], current_user_data: Mapping[str, Any]) -> Optional[Mapping[str, Any]]:
        current_user = User.parse_obj(current_user_data)
        book = BookData.parse_obj(book_data) 
        book.updated_by = current_user.id
        updated_book = book_service.update(id, book, current_user)
        return None if updated_book is None else updated_book.dict()


    @rpc.handle('delete_book')
    def delete_book(id: str, current_user_data: Mapping[str, Any]) -> Optional[Mapping[str, Any]]:
        current_user = User.parse_obj(current_user_data)
        book = book_service.delete(id, current_user)
        return None if book is None else book.dict()


    print('Handle RPC for library.Book', file=sys.stderr)