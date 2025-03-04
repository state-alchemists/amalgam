from fastapi.testclient import TestClient

from myapp.main import app
from myapp.test._util.access_token import get_admin_access_token


def test_read_book_by_id():
    client = TestClient(app, base_url="http://localhost")
    access_token = get_admin_access_token()
    new_book_data = {
        "isbn": "to-be-read-book",
    }
    insert_response = client.post(
        "/api/v1/books",
        json=new_book_data,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert insert_response.status_code == 200
    id = insert_response.json().get("id")
    # fetching
    response = client.get(
        f"/api/v1/books/{id}", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    response_data = response.json()
    assert response_data.get("id") == id
    assert response_data.get("isbn") == "to-be-read-book"


def test_read_book_bulk():
    client = TestClient(app, base_url="http://localhost")
    access_token = get_admin_access_token()
    new_first_book_data = {
        "isbn": "to-be-read-book-bulk-1",
    }
    new_second_book_data = {
        "isbn": "to-be-read-book-bulk-2",
    }
    new_book_data = [new_first_book_data, new_second_book_data]
    insert_response = client.post(
        "/api/v1/books/bulk",
        json=new_book_data,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert insert_response.status_code == 200
    ids = [row["id"] for row in insert_response.json()]
    # fetching
    response = client.get(
        f"/api/v1/books",
        params={
            "filter": "isbn:like:to-be-read-book-bulk-%",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_data_count = response.json()["count"]
    assert response_data_count == 2
    response_data = response.json()["data"]
    # Data should match
    assert len([row["id"] for row in response_data if row["id"] in ids]) == 2
    assert new_first_book_data["isbn"] in [row["isbn"] for row in response_data]
    assert new_second_book_data["isbn"] in [row["isbn"] for row in response_data]
