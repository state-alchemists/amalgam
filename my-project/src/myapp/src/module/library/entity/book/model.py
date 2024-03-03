from module.log.component.historical_repo_model import HistoricalRepoModel
from module.library.schema.book import (
    Book,
    BookData,
    BookResult,
)


class BookModel(
    HistoricalRepoModel[
        Book, BookData, BookResult
    ]
):
    schema_result_cls = BookResult
    log_entity_name = "book"
