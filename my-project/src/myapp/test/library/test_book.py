from collections.abc import AsyncIterator
from datetime import date, datetime, time

import pytest
from config import APP_AUTH_ADMIN_PASSWORD, APP_AUTH_ADMIN_USERNAME
from httpx import AsyncClient

inserted_success_data = {"code": "test-kebab-create-entity-name-success", 'title': "A string", 'page_number': 42, 'purchase_date': date(2024, 8, 10), 'available': True, 'synopsis': "A text"}
to_be_updated_success_data = {"code": "test-book-to-be-updated-success", 'title': "A string", 'page_number': 42, 'purchase_date': date(2024, 8, 10), 'available': True, 'synopsis': "A text"}
updated_success_data = {"code": "test-book-updated-success", 'title': "A string", 'page_number': 42, 'purchase_date': date(2024, 8, 10), 'available': True, 'synopsis': "A text"}
to_be_deleted_success_data = {"code": "test-book-to-be-deleted-success", 'title': "A string", 'page_number': 42, 'purchase_date': date(2024, 8, 10), 'available': True, 'synopsis': "A text"}


@pytest.mark.asyncio
async def test_insert_book_and_get_success(
    test_client_generator: AsyncIterator[AsyncClient],
):
    async for client in test_client_generator:
        # login
        login_admin_response = await client.post(
            "/api/v1/auth/login",
            json={
                "identity": APP_AUTH_ADMIN_USERNAME,
                "password": APP_AUTH_ADMIN_PASSWORD,
            },
        )
        assert login_admin_response.status_code == 200
        admin_access_token = login_admin_response.json().get("access_token", "")

        # create book
        create_response = await client.post(
            "/api/v1/library/books",
            json=inserted_success_data,
            headers={"Authorization": "Bearer " + admin_access_token},
        )
        assert create_response.status_code == 200
        json_create_response = create_response.json()
        create_response_id = json_create_response.get("id", "")
        assert create_response_id != ""

        # get_by_id
        get_by_id_response = await client.get(
            f"/api/v1/library/books/{create_response_id}",
            headers={"Authorization": "Bearer " + admin_access_token},
        )
        assert get_by_id_response.status_code == 200
        json_get_by_id_response = get_by_id_response.json()
        get_by_id_response_id = json_get_by_id_response.get("id", "")
        assert get_by_id_response_id == create_response_id

        # get
        get_response = await client.get(
            "/api/v1/library/books",
            headers={"Authorization": "Bearer " + admin_access_token},
        )
        assert get_response.status_code == 200
        json_get_response = get_response.json()
        get_response_count = json_get_response.get("count", "")
        assert get_response_count > 0
        get_response_data = json_get_response.get("data", [])
        get_created_response_data = [
            row for row in get_response_data if row["id"] == create_response_id
        ]
        assert len(get_created_response_data) == 1


@pytest.mark.asyncio
async def test_update_book_and_get_success(
    test_client_generator: AsyncIterator[AsyncClient],
):
    async for client in test_client_generator:
        # login
        login_admin_response = await client.post(
            "/api/v1/auth/login",
            json={
                "identity": APP_AUTH_ADMIN_USERNAME,
                "password": APP_AUTH_ADMIN_PASSWORD,
            },
        )
        assert login_admin_response.status_code == 200
        admin_access_token = login_admin_response.json().get("access_token", "")

        # create book
        create_response = await client.post(
            "/api/v1/library/books",
            json=to_be_updated_success_data,
            headers={"Authorization": "Bearer " + admin_access_token},
        )
        assert create_response.status_code == 200
        json_create_response = create_response.json()
        create_response_id = json_create_response.get("id", "")
        assert create_response_id != ""

        # update book
        update_response = await client.put(
            f"/api/v1/library/books/{create_response_id}",
            json=updated_success_data,
            headers={"Authorization": "Bearer " + admin_access_token},
        )
        assert update_response.status_code == 200
        json_update_response = update_response.json()
        update_response_id = json_update_response.get("id", "")
        assert update_response_id == create_response_id

        # get_by_id
        get_by_id_response = await client.get(
            f"/api/v1/library/books/{create_response_id}",
            headers={"Authorization": "Bearer " + admin_access_token},
        )
        assert get_by_id_response.status_code == 200
        json_get_by_id_response = get_by_id_response.json()
        get_by_id_response_id = json_get_by_id_response.get("id", "")
        assert get_by_id_response_id == create_response_id
        for key, expected_value in updated_success_data.items():
            actual_value = json_get_by_id_response.get(key, "")
            assert f"{key}:{actual_value}" == f"{key}:{expected_value}"

        # get
        get_response = await client.get(
            "/api/v1/library/books",
            headers={"Authorization": "Bearer " + admin_access_token},
        )
        assert get_response.status_code == 200
        json_get_response = get_response.json()
        get_response_count = json_get_response.get("count", "")
        assert get_response_count > 0
        get_response_data = json_get_response.get("data", [])
        get_created_response_data = [
            row for row in get_response_data if row["id"] == create_response_id
        ]
        assert len(get_created_response_data) == 1


@pytest.mark.asyncio
async def test_delete_book_and_get_success(
    test_client_generator: AsyncIterator[AsyncClient],
):
    async for client in test_client_generator:
        # login
        login_admin_response = await client.post(
            "/api/v1/auth/login",
            json={
                "identity": APP_AUTH_ADMIN_USERNAME,
                "password": APP_AUTH_ADMIN_PASSWORD,
            },
        )
        assert login_admin_response.status_code == 200
        admin_access_token = login_admin_response.json().get("access_token", "")

        # create book
        create_response = await client.post(
            "/api/v1/library/books",
            json=to_be_deleted_success_data,
            headers={"Authorization": "Bearer " + admin_access_token},
        )
        assert create_response.status_code == 200
        json_create_response = create_response.json()
        create_response_id = json_create_response.get("id", "")
        assert create_response_id != ""

        # create book
        delete_response = await client.delete(
            f"/api/v1/library/books/{create_response_id}",
            headers={"Authorization": "Bearer " + admin_access_token},
        )
        assert delete_response.status_code == 200
        json_delete_response = delete_response.json()
        delete_response_id = json_delete_response.get("id", "")
        assert delete_response_id == create_response_id

        # get_by_id
        get_by_id_response = await client.get(
            f"/api/v1/library/books/{create_response_id}",
            headers={"Authorization": "Bearer " + admin_access_token},
        )
        assert get_by_id_response.status_code == 404

        # get
        get_response = await client.get(
            "/api/v1/library/books",
            headers={"Authorization": "Bearer " + admin_access_token},
        )
        assert get_response.status_code == 200
        json_get_response = get_response.json()
        get_response_count = json_get_response.get("count", "")
        assert get_response_count > 0
        get_response_data = json_get_response.get("data", [])
        get_created_response_data = [
            row for row in get_response_data if row["id"] == create_response_id
        ]
        assert len(get_created_response_data) == 0
