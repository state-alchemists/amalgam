from abc import ABC, abstractmethod

from myapp.schema.book import (
    Book,
    BookCreateWithAudit,
    BookResponse,
    BookUpdateWithAudit,
)


class BookRepository(ABC):

    @abstractmethod
    async def get_by_id(self, id: str) -> BookResponse:
        """Get my entity by id"""

    @abstractmethod
    async def get_by_ids(self, id_list: list[str]) -> BookResponse:
        """Get my entities by ids"""

    @abstractmethod
    async def get(
        self,
        page: int = 1,
        page_size: int = 10,
        filter: str | None = None,
        sort: str | None = None,
    ) -> list[Book]:
        """Get my entities by filter and sort"""

    @abstractmethod
    async def count(self, filter: str | None = None) -> int:
        """Count my entities by filter"""

    @abstractmethod
    async def create(self, data: BookCreateWithAudit) -> Book:
        """Create a new my entity"""

    @abstractmethod
    async def create_bulk(self, data: list[BookCreateWithAudit]) -> list[Book]:
        """Create some my entities"""

    @abstractmethod
    async def delete(self, id: str) -> Book:
        """Delete a my entity"""

    @abstractmethod
    async def delete_bulk(self, id_list: list[str]) -> list[Book]:
        """Delete some my entities"""

    @abstractmethod
    async def update(self, id: str, data: BookUpdateWithAudit) -> Book:
        """Update a my entity"""

    @abstractmethod
    async def update_bulk(
        self, id_list: list[str], data: BookUpdateWithAudit
    ) -> list[Book]:
        """Update some my entities"""
