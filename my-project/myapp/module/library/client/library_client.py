from abc import ABC, abstractmethod

from myapp.schema.book import (
    BookCreate,
    BookCreateWithAudit,
    BookResponse,
    BookUpdate,
    BookUpdateWithAudit,
    MultipleBookResponse,
)


class LibraryClient(ABC):
    """
    Defining client methods
    """

    @abstractmethod
    async def get_book_by_id(self, book_id: str) -> BookResponse:
        """Get my entity by id"""

    @abstractmethod
    async def get_books(
        self,
        page: int = 1,
        page_size: int = 10,
        sort: str | None = None,
        filter: str | None = None,
    ) -> MultipleBookResponse:
        """Get my entities by filter and sort"""

    @abstractmethod
    async def create_book_bulk(
        self, data: list[BookCreateWithAudit]
    ) -> list[BookResponse]:
        """Create new my entities"""

    @abstractmethod
    async def create_book(self, data: BookCreateWithAudit) -> BookResponse:
        """Create a new my entities"""

    @abstractmethod
    async def update_book_bulk(
        self, book_ids: list[str], data: BookUpdateWithAudit
    ) -> BookResponse:
        """Update some my entities"""

    @abstractmethod
    async def update_book(
        self, book_id: str, data: BookUpdateWithAudit
    ) -> BookResponse:
        """Update a my entity"""

    @abstractmethod
    async def delete_book_bulk(self, book_ids: str, deleted_by: str) -> BookResponse:
        """Delete some my entities"""

    @abstractmethod
    async def delete_book(self, book_id: str, deleted_by: str) -> BookResponse:
        """Delete a my entity"""
