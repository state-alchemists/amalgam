from component.messagebus import publisher
from module.library.component.repo.book_repo import (
    book_repo,
)
from module.library.entity.book.model import (
    BookModel,
)

book_model: BookModel = BookModel(
    book_repo, publisher
)
