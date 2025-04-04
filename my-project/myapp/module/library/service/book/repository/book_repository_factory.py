from myapp.common.db_engine_factory import db_engine
from myapp.config import APP_REPOSITORY_TYPE
from myapp.module.library.service.book.repository.book_db_repository import (
    BookDBRepository,
)
from myapp.module.library.service.book.repository.book_repository import (
    BookRepository,
)

if APP_REPOSITORY_TYPE == "db":
    book_repository: BookRepository = BookDBRepository(db_engine)
else:
    book_repository: BookRepository = None
