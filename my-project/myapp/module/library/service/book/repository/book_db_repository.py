from passlib.context import CryptContext

from myapp.common.base_db_repository import BaseDBRepository
from myapp.module.library.service.book.repository.book_repository import BookRepository
from myapp.schema.book import (
    Book,
    BookCreateWithAudit,
    BookResponse,
    BookUpdateWithAudit,
)


class BookDBRepository(
    BaseDBRepository[
        Book,
        BookResponse,
        BookCreateWithAudit,
        BookUpdateWithAudit,
    ],
    BookRepository,
):
    db_model = Book
    response_model = BookResponse
    create_model = BookCreateWithAudit
    update_model = BookUpdateWithAudit
    entity_name = "book"
    column_preprocessors = {}
