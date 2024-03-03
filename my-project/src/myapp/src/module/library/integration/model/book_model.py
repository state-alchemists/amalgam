from integration.messagebus import publisher
from module.library.entity.book.model import (
    BookModel,
)
from module.library.integration.repo.book_repo import (
    book_repo,
)

book_model: BookModel = BookModel(
    book_repo, publisher
)
