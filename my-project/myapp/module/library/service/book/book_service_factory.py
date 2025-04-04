from myapp.common.logger_factory import logger
from myapp.module.library.service.book.book_service import (
    BookService,
)
from myapp.module.library.service.book.repository.book_repository_factory import (
    book_repository,
)

book_service = BookService(logger, book_repository=book_repository)
