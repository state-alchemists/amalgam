from module.library.book.test_book_service_util import (
    create_book_data,
    insert_book_data,
    init_test_book_service_components
)
from module.auth.user.test_default_user_service_util import AUTHORIZED_ACTIVE_USER


def test_book_service_crud_find_by_id_existing():
    book_service, book_repo, _, _ = init_test_book_service_components()
    # prepare repo
    existing_book = insert_book_data(
        book_repo)
    # test find by id (existing)
    fetched_book = book_service.find_by_id(
        existing_book.id, AUTHORIZED_ACTIVE_USER)
    assert fetched_book is not None
    assert fetched_book.id == existing_book.id
    assert fetched_book.title == 'book'
    assert fetched_book.created_by == 'original_user'
    assert fetched_book.updated_by == 'original_user'


def test_book_service_crud_find_by_id_non_existing():
    book_service, book_repo, _, _ = init_test_book_service_components()
    # prepare repo
    insert_book_data(book_repo)
    # test find by id (non existing)
    is_error = False
    try:
        book_service.find_by_id(
            'invalid-id', AUTHORIZED_ACTIVE_USER
        )
    except Exception:
        is_error = True
    assert is_error


def test_book_service_crud_find_existing():
    book_service, book_repo, _, _ = init_test_book_service_components()
    # prepare repo
    existing_book = insert_book_data(
        book_repo
    )
    # test find (existing)
    fetched_book_result = book_service.find(
        keyword='book',
        limit=100,
        offset=0,
        current_user=AUTHORIZED_ACTIVE_USER
    )
    assert fetched_book_result.count == 1
    fetched_book = fetched_book_result.rows[0]
    assert fetched_book is not None
    assert fetched_book.id == existing_book.id
    assert fetched_book.title == 'book'
    assert fetched_book.created_by == 'original_user'
    assert fetched_book.updated_by == 'original_user'


def test_book_service_crud_find_non_existing():
    book_service, book_repo, _, _ = init_test_book_service_components()
    # prepare repo
    insert_book_data(book_repo)
    # test find (non existing)
    non_existing_book_result = book_service.find(
        keyword='invalid-keyword', limit=100, offset=0,
        current_user=AUTHORIZED_ACTIVE_USER
    )
    assert non_existing_book_result.count == 0


def test_book_service_crud_find_pagination():
    book_service, book_repo, _, _ = init_test_book_service_components()
    # prepare repo
    for index in range(7):
        insert_book_data(book_repo, index)
    # test find (page 1)
    fetched_book_result = book_service.find(
        keyword='book', limit=3, offset=0,
        current_user=AUTHORIZED_ACTIVE_USER
    )
    assert len(fetched_book_result.rows) == 3
    assert fetched_book_result.count == 7
    # test find (page 2)
    fetched_book_result = book_service.find(
        keyword='book', limit=3, offset=3,
        current_user=AUTHORIZED_ACTIVE_USER
    )
    assert len(fetched_book_result.rows) == 3
    assert fetched_book_result.count == 7
    # test find (page 3)
    fetched_book_result = book_service.find(
        keyword='book', limit=3, offset=6,
        current_user=AUTHORIZED_ACTIVE_USER
    )
    assert len(fetched_book_result.rows) == 1
    assert fetched_book_result.count == 7


def test_book_service_crud_insert():
    book_service, book_repo, _, _ = init_test_book_service_components()
    # prepare insert
    inserted_book_data = create_book_data()
    inserted_book_data.title = 'book'
    inserted_book_data.created_by = 'original_user'
    inserted_book_data.updated_by = 'original_user'
    # test insert
    inserted_book = book_service.insert(
        inserted_book_data, AUTHORIZED_ACTIVE_USER
    )
    assert inserted_book is not None
    assert inserted_book.id != ''
    assert inserted_book.title == 'book'
    assert inserted_book.created_by == AUTHORIZED_ACTIVE_USER.id
    assert inserted_book.updated_by == AUTHORIZED_ACTIVE_USER.id
    assert book_repo.count(keyword='') == 1


def test_book_service_crud_update_existing():
    book_service, book_repo, _, _ = init_test_book_service_components()
    # prepare repo
    existing_book = insert_book_data(
        book_repo
    )
    # test update (existing)
    updated_book_data = create_book_data()
    updated_book_data.title = 'updated'
    updated_book_data.updated_by = 'editor'
    updated_book = book_service.update(
        existing_book.id,
        updated_book_data,
        AUTHORIZED_ACTIVE_USER
    )
    assert updated_book is not None
    assert updated_book.id == existing_book.id
    assert updated_book.title == 'updated'
    assert updated_book.created_by == 'original_user'
    assert updated_book.updated_by == AUTHORIZED_ACTIVE_USER.id
    assert book_repo.count(keyword='') == 1


def test_book_service_crud_update_non_existing():
    book_service, book_repo, _, _ = init_test_book_service_components()
    # prepare repo
    insert_book_data(book_repo)
    # test update (non existing)
    updated_book_data = create_book_data()
    updated_book_data.title = 'updated'
    updated_book_data.updated_by = 'editor'
    is_error = False
    try:
        book_service.update(
            'invalid-id',
            updated_book_data,
            AUTHORIZED_ACTIVE_USER
        )
    except Exception:
        is_error = True
    assert is_error
    assert book_repo.count(keyword='') == 1


def test_book_service_crud_delete_existing():
    book_service, book_repo, _, _ = init_test_book_service_components()
    # prepare repo
    existing_book = insert_book_data(
        book_repo)
    # test find by id (existing)
    deleted_book = book_service.delete(
        existing_book.id, AUTHORIZED_ACTIVE_USER
    )
    assert deleted_book is not None
    assert deleted_book.id == existing_book.id
    assert deleted_book.title == 'book'
    assert deleted_book.created_by == 'original_user'
    assert deleted_book.updated_by == 'original_user'
    assert book_repo.count(keyword='') == 0


def test_book_service_crud_delete_non_existing():
    book_service, book_repo, _, _ = init_test_book_service_components()
    # prepare repo
    insert_book_data(book_repo)
    # test find by id (non existing)
    is_error = False
    try:
        book_service.delete(
            'invalid-id', AUTHORIZED_ACTIVE_USER
        )
    except Exception:
        is_error = True
    assert is_error
    assert book_repo.count(keyword='') == 1
