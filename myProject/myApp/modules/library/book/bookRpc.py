from typing import Any, Optional, Mapping
from helpers.transport import RPC
from schemas.book import Book, BookData
from schemas.user import User
from modules.library.book.repos.bookRepo import BookRepo
from modules.library.book.bookService import BookService

def register_book_entity_rpc(rpc: RPC, book_repo: BookRepo):

    book_service = BookService(book_repo)

    @rpc.handle('find_book')
    def find_books(keyword: str, limit: int, offset: int) -> Mapping[str, Any]:
        book_result = book_service.find(keyword, limit, offset)
        return book_result.dict()

    @rpc.handle('find_book_by_id')
    def find_book_by_id(id: str) -> Optional[Mapping[str, Any]]:
        book = book_service.find_by_id(id)
        return None if book is None else book.dict()

    @rpc.handle('insert_book')
    def insert_book(book_data: Mapping[str, Any], current_user_data: Mapping[str, Any]) -> Optional[Mapping[str, Any]]:
        current_user = User.parse_obj(current_user_data)
        book = BookData.parse_obj(book_data) 
        book.created_by = current_user.id
        new_book = book_service.insert(book)
        return None if new_book is None else new_book.dict()

    @rpc.handle('update_book')
    def update_book(id: str, book_data: Mapping[str, Any], current_user_data: Mapping[str, Any]) -> Optional[Mapping[str, Any]]:
        current_user = User.parse_obj(current_user_data)
        book = BookData.parse_obj(book_data) 
        book.updated_by = current_user.id
        updated_book = book_service.update(id, book)
        return None if updated_book is None else updated_book.dict()

    @rpc.handle('delete_book')
    def delete_book(id: str, current_user_data: Mapping[str, Any]) -> Optional[Mapping[str, Any]]:
        book = book_service.delete(id)
        return None if book is None else book.dict()

    print('Handle RPC for library.Book')