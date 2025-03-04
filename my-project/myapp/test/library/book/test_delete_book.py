from fastapi.testclient import TestClient

from myapp.main import app
from myapp.test._util.access_token import get_admin_access_token


def test_delete_book():
    client = TestClient(app, base_url="http://localhost")
    access_token = get_admin_access_token()
    new_book_data = {
        "isbn": "to-be-deleted-book",
    }
    insert_response = client.post(
        "/api/v1/books",
        json=new_book_data,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert insert_response.status_code == 200
    id = insert_response.json().get("id")
    # deleting
    response = client.delete(
        f"/api/v1/books/{id}", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    response_data = response.json()
    assert response_data.get("id") == id
    assert response_data.get("isbn") == "to-be-deleted-book"


def test_delete_book_bulk():
    client = TestClient(app, base_url="http://localhost")
    access_token = get_admin_access_token()
    new_first_book_data = {
        "isbn": "to-be-deleted-book-bulk-1",
    }
    new_second_book_data = {
        "isbn": "to-be-deleted-book-bulk-2",
    }
    new_book_data = [new_first_book_data, new_second_book_data]
    insert_response = client.post(
        "/api/v1/books/bulk",
        json=new_book_data,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert insert_response.status_code == 200
    ids = [row["id"] for row in insert_response.json()]
    # deleting (use client.request since client.delete doesn't support json param)
    response = client.request(
        "DELETE",
        f"/api/v1/books/bulk",
        json=ids,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_data = response.json()
    # Data should match
    assert len([row["id"] for row in response_data if row["id"] in ids]) == 2
    assert new_first_book_data["isbn"] in [row["isbn"] for row in response_data]
    assert new_second_book_data["isbn"] in [row["isbn"] for row in response_data]
