from typing import Optional, List
from modules.library.book.bookService import BookService
from modules.library.book.repos.bookRepo import BookRepo
from schemas.book import Book, BookData
from helpers.transport import LocalRPC, LocalMessageBus

################################################
# -- ⚙️ Mock data and objects
################################################

mock_book_data = BookData(
    synopsis='',
    title='',
    author='',
    created_by='mock_user_id'
)

mock_book = Book(
    synopsis='',
    title='',
    author='',
    id='mock_book_id',
    created_by='mock_user_id',
    updated_by='mock_user_id'
)

class MockBookRepo(BookRepo):

    def __init__(self):
        self.book_data: Optional[BookData] = None
        self.find_id: Optional[str] = None
        self.find_keyword: Optional[str] = None
        self.count_keyword: Optional[str] = None
        self.find_limit: Optional[int] = None
        self.find_offset: Optional[int] = None
        self.insert_book_data: Optional[BookData] = None
        self.update_id: Optional[str] = None
        self.update_book_data: Optional[BookData] = None
        self.delete_id: Optional[str] = None

    def find_by_id(self, id: str) -> Optional[Book]:
        self.find_id = id
        return mock_book

    def find(self, keyword: str, limit: str, offset: int) -> List[Book]:
        self.find_keyword = keyword
        self.find_limit = limit
        self.find_offset = offset
        return [mock_book]

    def count(self, keyword: str) -> int:
        self.count_keyword = keyword
        return 1

    def insert(self, book_data: BookData) -> Optional[Book]:
        self.insert_book_data = book_data
        return mock_book

    def update(self, id: str, book_data: BookData) -> Optional[Book]:
        self.update_id = id
        self.update_book_data = book_data
        return mock_book

    def delete(self, id: str) -> Optional[Book]:
        self.delete_id = id
        return mock_book


################################################
# -- 🧪 Test
################################################

def test_book_service_find():
    mock_mb = LocalMessageBus()
    mock_rpc = LocalRPC()
    mock_book_repo = MockBookRepo()
    book_service = BookService(mock_mb, mock_rpc, mock_book_repo)
    book_result = book_service.find('find_keyword', 73, 37)
    # make sure all parameters are passed to repo
    assert mock_book_repo.find_keyword == 'find_keyword'
    assert mock_book_repo.find_limit == 73
    assert mock_book_repo.find_offset == 37
    assert mock_book_repo.count_keyword == 'find_keyword'
    # make sure book_service return the result correctly
    assert book_result.count == 1
    assert len(book_result.rows) == 1
    assert book_result.rows[0] == mock_book


def test_book_service_find_by_id():
    mock_mb = LocalMessageBus()
    mock_rpc = LocalRPC()
    mock_book_repo = MockBookRepo()
    book_service = BookService(mock_mb, mock_rpc, mock_book_repo)
    book = book_service.find_by_id('find_id')
    # make sure all parameters are passed to repo
    assert mock_book_repo.find_id == 'find_id'
    # make sure book_service return the result correctly
    assert book == mock_book


def test_book_service_insert():
    mock_mb = LocalMessageBus()
    mock_rpc = LocalRPC()
    mock_book_repo = MockBookRepo()
    book_service = BookService(mock_mb, mock_rpc, mock_book_repo)
    new_book = book_service.insert(mock_book_data)
    # make sure all parameters are passed to repo
    assert mock_book_repo.insert_book_data == mock_book_data
    # make sure book_service return the result correctly
    assert new_book == mock_book


def test_book_service_update():
    mock_mb = LocalMessageBus()
    mock_rpc = LocalRPC()
    mock_book_repo = MockBookRepo()
    book_service = BookService(mock_mb, mock_rpc, mock_book_repo)
    updated_book = book_service.update('update_id', mock_book_data)
    # make sure all parameters are passed to repo
    assert mock_book_repo.update_id == 'update_id'
    assert mock_book_repo.update_book_data == mock_book_data
    # make sure book_service return the result correctly
    assert updated_book == mock_book


def test_book_service_delete():
    mock_mb = LocalMessageBus()
    mock_rpc = LocalRPC()
    mock_book_repo = MockBookRepo()
    book_service = BookService(mock_mb, mock_rpc, mock_book_repo)
    deleted_book = book_service.delete('delete_id')
    # make sure all parameters are passed to repo
    assert mock_book_repo.delete_id == 'delete_id'
    # make sure book_service return the result correctly
    assert deleted_book == mock_book

