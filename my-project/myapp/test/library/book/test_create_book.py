from fastapi.testclient import TestClient

from myapp.main import app
from myapp.test._util.access_token import get_admin_access_token


def test_create_book():
    client = TestClient(app, base_url="http://localhost")
    access_token = get_admin_access_token()
    new_book_data = {
        "isbn": "new-book",
    }
    response = client.post(
        "/api/v1/books",
        json=new_book_data,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_data = response.json()
    assert response_data.get("id") is not None
    assert response_data.get("id") != ""
    assert response_data.get("isbn") == "new-book"


def test_create_book_bulk():
    client = TestClient(app, base_url="http://localhost")
    access_token = get_admin_access_token()
    new_first_book_data = {
        "isbn": "new-book-bulk-1",
    }
    new_second_book_data = {
        "isbn": "new-book-bulk-2",
    }
    new_book_data = [new_first_book_data, new_second_book_data]
    response = client.post(
        "/api/v1/books/bulk",
        json=new_book_data,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == 2
    # Id should not be empty
    assert response_data[0] is not None
    assert response_data[0] != ""
    assert response_data[1] is not None
    assert response_data[1] != ""
    # Data should match
    assert new_first_book_data["isbn"] in [row["isbn"] for row in response_data]
    assert new_second_book_data["isbn"] in [row["isbn"] for row in response_data]
