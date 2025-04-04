from logging import Logger

from myapp.common.base_service import BaseService
from myapp.module.library.service.book.repository.book_repository import (
    BookRepository,
)
from myapp.schema.book import (
    BookCreateWithAudit,
    BookResponse,
    BookUpdateWithAudit,
    MultipleBookResponse,
)


class BookService(BaseService):

    def __init__(self, logger: Logger, book_repository: BookRepository):
        super().__init__(logger)
        self.book_repository = book_repository

    @BaseService.route(
        "/api/v1/books/{book_id}",
        methods=["get"],
        response_model=BookResponse,
    )
    async def get_book_by_id(self, book_id: str) -> BookResponse:
        return await self.book_repository.get_by_id(book_id)

    @BaseService.route(
        "/api/v1/books",
        methods=["get"],
        response_model=MultipleBookResponse,
    )
    async def get_books(
        self,
        page: int = 1,
        page_size: int = 10,
        sort: str | None = None,
        filter: str | None = None,
    ) -> MultipleBookResponse:
        books = await self.book_repository.get(page, page_size, filter, sort)
        count = await self.book_repository.count(filter)
        return MultipleBookResponse(data=books, count=count)

    @BaseService.route(
        "/api/v1/books/bulk",
        methods=["post"],
        response_model=list[BookResponse],
    )
    async def create_book_bulk(
        self, data: list[BookCreateWithAudit]
    ) -> list[BookResponse]:
        books = await self.book_repository.create_bulk(data)
        return await self.book_repository.get_by_ids([book.id for book in books])

    @BaseService.route(
        "/api/v1/books",
        methods=["post"],
        response_model=BookResponse,
    )
    async def create_book(self, data: BookCreateWithAudit) -> BookResponse:
        book = await self.book_repository.create(data)
        return await self.book_repository.get_by_id(book.id)

    @BaseService.route(
        "/api/v1/books/bulk",
        methods=["put"],
        response_model=list[BookResponse],
    )
    async def update_book_bulk(
        self, book_ids: list[str], data: BookUpdateWithAudit
    ) -> list[BookResponse]:
        await self.book_repository.update_bulk(book_ids, data)
        return await self.book_repository.get_by_ids(book_ids)

    @BaseService.route(
        "/api/v1/books/{book_id}",
        methods=["put"],
        response_model=BookResponse,
    )
    async def update_book(
        self, book_id: str, data: BookUpdateWithAudit
    ) -> BookResponse:
        await self.book_repository.update(book_id, data)
        return await self.book_repository.get_by_id(book_id)

    @BaseService.route(
        "/api/v1/books/bulk",
        methods=["delete"],
        response_model=list[BookResponse],
    )
    async def delete_book_bulk(
        self, book_ids: list[str], deleted_by: str
    ) -> list[BookResponse]:
        books = await self.book_repository.get_by_ids(book_ids)
        await self.book_repository.delete_bulk(book_ids)
        return books

    @BaseService.route(
        "/api/v1/books/{book_id}",
        methods=["delete"],
        response_model=BookResponse,
    )
    async def delete_book(self, book_id: str, deleted_by: str) -> BookResponse:
        book = await self.book_repository.get_by_id(book_id)
        await self.book_repository.delete(book_id)
        return book
