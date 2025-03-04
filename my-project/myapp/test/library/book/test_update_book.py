from fastapi.testclient import TestClient

from myapp.main import app
from myapp.test._util.access_token import get_admin_access_token


def test_update_book():
    client = TestClient(app, base_url="http://localhost")
    access_token = get_admin_access_token()
    new_book_data = {
        "isbn": "to-be-updated-book",
    }
    insert_response = client.post(
        "/api/v1/books",
        json=new_book_data,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert insert_response.status_code == 200
    id = insert_response.json().get("id")
    # updating
    updated_book_data = {
        "isbn": "updated-book",
    }
    response = client.put(
        f"/api/v1/books/{id}",
        json=updated_book_data,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_data = response.json()
    assert response_data.get("id") == id
    assert response_data.get("isbn") == "updated-book"


def test_update_book_bulk():
    client = TestClient(app, base_url="http://localhost")
    access_token = get_admin_access_token()
    new_first_book_data = {
        "isbn": "to-be-updated-book-bulk-1",
    }
    insert_response = client.post(
        "/api/v1/books/bulk",
        json=[new_first_book_data],
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert insert_response.status_code == 200
    ids = [row["id"] for row in insert_response.json()]
    # updating (we only test with one data)
    updated_book_data = {"isbn": "updated-book-bulk-1"}
    response = client.put(
        f"/api/v1/books/bulk",
        json={
            "book_ids": ids,
            "data": updated_book_data,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == 1
    response_data[0].get("id") == ids[0]
    response_data[0].get("isbn") == updated_book_data["isbn"]
