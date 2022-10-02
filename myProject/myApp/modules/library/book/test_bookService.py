from typing import Optional, List
from modules.library.book.bookService import BookService
from modules.library.book.repos.dbBookRepo import DBBookRepo
from schemas.book import BookData, BookData
from helpers.transport import LocalRPC, LocalMessageBus

from sqlalchemy import create_engine

################################################
# -- ⚙️ Helpers
################################################

def create_book_data():
    dummy_book_data = BookData(
        synopsis='',
        title='',
        author='',
    )
    return dummy_book_data


################################################
# -- 🧪 Test
################################################

def test_book_service():
    engine = create_engine('sqlite://', echo=True)
    book_repo = DBBookRepo(engine=engine, create_all=True)
    mb = LocalMessageBus()
    rpc = LocalRPC()
    book_service = BookService(mb, rpc, book_repo)

    # prepare insert
    inserted_book_data = create_book_data()
    inserted_book_data.title = 'original'
    inserted_book_data.created_by = 'original_user'
    inserted_book_data.updated_by = 'original_user'
    # test insert
    inserted_book = book_service.insert(inserted_book_data)
    assert inserted_book is not None
    assert inserted_book.id != '' 
    assert inserted_book.title == 'original'
    assert inserted_book.created_by == 'original_user'
    assert inserted_book.updated_by == 'original_user'

    # test find by id (existing, after insert)
    existing_book = book_service.find_by_id(inserted_book.id)
    assert existing_book is not None
    assert existing_book.id == inserted_book.id
    assert existing_book.title == inserted_book.title
    assert existing_book.created_by == inserted_book.created_by
    assert existing_book.updated_by == inserted_book.updated_by

    # test find by id (non existing)
    non_existing_book = book_service.find_by_id('invalid_id')
    assert non_existing_book is None

    # prepare update (existing)
    updated_book_data = create_book_data()
    updated_book_data.title = 'updated'
    updated_book_data.updated_by = 'editor'
    # test update (existing)
    updated_book = book_service.update(inserted_book.id, updated_book_data)
    assert updated_book is not None
    assert updated_book.id == inserted_book.id
    assert updated_book.title == 'updated'
    assert updated_book.created_by == 'original_user'
    assert updated_book.updated_by == 'editor'

    # test update (non existing)
    non_existing_book = book_service.update('invalid_id', updated_book_data)
    assert non_existing_book is None

    # test find by id (existing, after insert)
    existing_book = book_service.find_by_id(updated_book.id)
    assert existing_book is not None
    assert existing_book.id == inserted_book.id
    assert existing_book.title == 'updated'
    assert existing_book.created_by == 'original_user'
    assert existing_book.updated_by == 'editor'

    # test find (before delete, correct keyword)
    existing_result = book_service.find(keyword='updated', limit=10, offset=0)
    assert existing_result.count == 1
    assert len(existing_result.rows) == 1
    assert existing_result.rows[0].id == inserted_book.id

    # test find (before delete, incorrect keyword)
    non_existing_result = book_service.find(keyword='incorrect', limit=10, offset=0)
    assert non_existing_result.count == 0
    assert len(non_existing_result.rows) == 0

    # test delete existing
    deleted_book = book_service.delete(inserted_book.id)
    assert deleted_book is not None
    assert deleted_book.id == inserted_book.id
    assert deleted_book.title == 'updated'
    assert deleted_book.created_by == 'original_user'
    assert deleted_book.updated_by == 'editor'

    # test delete (non existing)
    non_existing_book = book_service.delete('invalid_id')
    assert non_existing_book is None

    # test find (after delete, correct keyword)
    non_existing_result = book_service.find(keyword='updated', limit=10, offset=0)
    assert non_existing_result.count == 0
    assert len(non_existing_result.rows) == 0
    