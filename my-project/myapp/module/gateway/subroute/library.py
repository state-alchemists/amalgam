import os
from typing import Annotated

from fastapi import Depends, FastAPI

from myapp.common.error import ForbiddenError
from myapp.module.gateway.util.auth import get_current_user
from myapp.module.gateway.util.view import render_content, render_error
from myapp.module.library.client.library_client_factory import library_client
from myapp.schema.book import BookCreate, BookResponse, BookUpdate, MultipleBookResponse
from myapp.schema.user import AuthUserResponse


def serve_library_route(app: FastAPI):
    """
    Serving routes for library
    """

    @app.get("/library/books", include_in_schema=False)
    def books_crud_ui(
        current_user: Annotated[AuthUserResponse, Depends(get_current_user)],
        page: int = 1,
        page_size: int = 10,
        sort: str | None = None,
        filter: str | None = None,
    ):
        if not current_user.has_permission("book:read"):
            return render_error(error_message="Access denied", status_code=403)
        return render_content(
            view_path=os.path.join("library", "book.html"),
            current_user=current_user,
            page_name="library.book",
            page=page,
            page_size=page_size,
            sort=sort,
            filter=filter,
            allow_create=current_user.has_permission("book:create"),
            allow_update=current_user.has_permission("book:update"),
            allow_delete=current_user.has_permission("book:delete"),
        )

    @app.get("/api/v1/books", response_model=MultipleBookResponse)
    async def get_books(
        current_user: Annotated[AuthUserResponse, Depends(get_current_user)],
        page: int = 1,
        page_size: int = 10,
        sort: str | None = None,
        filter: str | None = None,
    ) -> MultipleBookResponse:
        if not current_user.has_permission("book:read"):
            raise ForbiddenError("Access denied")
        return await library_client.get_books(
            page=page, page_size=page_size, sort=sort, filter=filter
        )

    @app.get("/api/v1/books/{book_id}", response_model=BookResponse)
    async def get_book_by_id(
        current_user: Annotated[AuthUserResponse, Depends(get_current_user)],
        book_id: str,
    ) -> BookResponse:
        if not current_user.has_permission("book:read"):
            raise ForbiddenError("Access denied")
        return await library_client.get_book_by_id(book_id)

    @app.post(
        "/api/v1/books/bulk",
        response_model=list[BookResponse],
    )
    async def create_book_bulk(
        current_user: Annotated[AuthUserResponse, Depends(get_current_user)],
        data: list[BookCreate],
    ) -> list[BookResponse]:
        if not current_user.has_permission("book:create"):
            raise ForbiddenError("Access denied")
        return await library_client.create_book_bulk(
            [row.with_audit(created_by=current_user.id) for row in data]
        )

    @app.post(
        "/api/v1/books",
        response_model=BookResponse,
    )
    async def create_book(
        current_user: Annotated[AuthUserResponse, Depends(get_current_user)],
        data: BookCreate,
    ) -> BookResponse:
        if not current_user.has_permission("book:create"):
            raise ForbiddenError("Access denied")
        return await library_client.create_book(
            data.with_audit(created_by=current_user.id)
        )

    @app.put(
        "/api/v1/books/bulk",
        response_model=list[BookResponse],
    )
    async def update_book_bulk(
        current_user: Annotated[AuthUserResponse, Depends(get_current_user)],
        book_ids: list[str],
        data: BookUpdate,
    ) -> list[BookResponse]:
        if not current_user.has_permission("book:update"):
            raise ForbiddenError("Access denied")
        return await library_client.update_book_bulk(
            book_ids, data.with_audit(updated_by=current_user.id)
        )

    @app.put(
        "/api/v1/books/{book_id}",
        response_model=BookResponse,
    )
    async def update_book(
        current_user: Annotated[AuthUserResponse, Depends(get_current_user)],
        book_id: str,
        data: BookUpdate,
    ) -> BookResponse:
        if not current_user.has_permission("book:update"):
            raise ForbiddenError("Access denied")
        return await library_client.update_book(
            book_id, data.with_audit(updated_by=current_user.id)
        )

    @app.delete(
        "/api/v1/books/bulk",
        response_model=list[BookResponse],
    )
    async def delete_book_bulk(
        current_user: Annotated[AuthUserResponse, Depends(get_current_user)],
        book_ids: list[str],
    ) -> list[BookResponse]:
        if not current_user.has_permission("book:delete"):
            raise ForbiddenError("Access denied")
        return await library_client.delete_book_bulk(
            book_ids, deleted_by=current_user.id
        )

    @app.delete(
        "/api/v1/books/{book_id}",
        response_model=BookResponse,
    )
    async def delete_book(
        current_user: Annotated[AuthUserResponse, Depends(get_current_user)],
        book_id: str,
    ) -> BookResponse:
        if not current_user.has_permission("book:delete"):
            raise ForbiddenError("Access denied")
        return await library_client.delete_book(book_id, deleted_by=current_user.id)
