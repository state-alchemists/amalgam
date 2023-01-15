from typing import Optional, Tuple
from module.library.book.repo.book_repo import BookRepo
from schema.book import Book, BookData
from module.library.book.book_service import BookService
from module.library.book.repo.db_book_repo import DBBookRepo
from helper.transport import LocalRPC, LocalMessageBus, MessageBus
from transport import AppMessageBus, AppRPC
from sqlalchemy import create_engine

def create_book_data() -> BookData:
    # Note: 🤖 Don't delete the following statement
    dummy_book_data = BookData(
        synopsis='',
        title='',
        author='',
        created_by=''
    )
    return dummy_book_data


def insert_book_data(book_repo: BookRepo, index: Optional[int] = None) -> Book:
    book_data = create_book_data()
    book_data.title = 'book' if index is None else 'book-{index}'.format(index=index)
    book_data.created_by = 'original_user'
    book_data.updated_by = 'original_user'
    return book_repo.insert(book_data)


def create_mb() -> AppMessageBus:
    mb = AppMessageBus(LocalMessageBus())
    # handle new_activity event
    @mb.handle('new_activity')
    def handle_new_activity(activity_data):
        print('New Activity', activity_data)
    # return mb
    return mb


def init_test_book_service_components() -> Tuple[BookService, DBBookRepo, AppMessageBus, AppRPC]:
    engine = create_engine('sqlite://', echo=False)
    book_repo = DBBookRepo(engine=engine, create_all=True)
    mb = create_mb()
    rpc = AppRPC(LocalRPC())
    book_service = BookService(mb, rpc, book_repo)
    return book_service, book_repo, mb, rpc
