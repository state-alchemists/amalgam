from typing import Any, List, Mapping, Optional
from core import AuthService, MenuService
from transport import AppMessageBus, AppRPC
from fastapi import Depends, FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from schema.book import (
    Book, BookData, BookResult
)
from schema.menu_context import MenuContext
from schema.user import User
from schema.auth_type import AuthType

import logging


################################################
# -- ⚙️ API
################################################
def register_book_api_route(
    app: FastAPI,
    mb: AppMessageBus,
    rpc: AppRPC,
    auth_service: AuthService
):

    @app.get(
        '/api/v1/books',
        response_model=BookResult
    )
    async def find_books(
        keyword: str = '',
        limit: int = 100,
        offset: int = 0,
        current_user: Optional[User] = Depends(
            auth_service.has_permission('api:book:read')
        )
    ) -> BookResult:
        '''
        Serving API to find books by keyword.
        '''
        result = {}
        try:
            current_user = _get_user_or_guest(current_user)
            result = rpc.call(
                'find_book',
                keyword, limit, offset, current_user.dict()
            )
        except HTTPException as http_exception:
            raise http_exception
        except Exception:
            _handle_non_http_exception()
        return BookResult.parse_obj(result)

    @app.get(
        '/api/v1/books/{id}',
        response_model=Book
    )
    async def find_book_by_id(
        id: str,
        current_user: Optional[User] = Depends(
            auth_service.has_permission('api:book:read')
        )
    ) -> Book:
        '''
        Serving API to find book by id.
        '''
        book = None
        try:
            current_user = _get_user_or_guest(current_user)
            book = rpc.call(
                'find_book_by_id',
                id, current_user.dict()
            )
        except HTTPException as http_exception:
            raise http_exception
        except Exception:
            _handle_non_http_exception()
        return Book.parse_obj(book)

    @app.post(
        '/api/v1/books',
        response_model=Book
    )
    async def insert_book(
        book_data: BookData,
        current_user: Optional[User] = Depends(
            auth_service.has_permission('api:book:create')
        )
    ) -> Book:
        '''
        Serving API to insert new book.
        '''
        book = None
        try:
            current_user = _get_user_or_guest(current_user)
            book = rpc.call(
                'insert_book',
                book_data.dict(), current_user.dict()
            )
        except HTTPException as http_exception:
            raise http_exception
        except Exception:
            _handle_non_http_exception()
        return Book.parse_obj(book)

    @app.put(
        '/api/v1/books/{id}',
        response_model=Book
    )
    async def update_book(
        id: str,
        book_data: BookData,
        current_user: Optional[User] = Depends(
            auth_service.has_permission('api:book:update')
        )
    ) -> Book:
        '''
        Serving API to update book by id.
        '''
        book = None
        try:
            current_user = _get_user_or_guest(current_user)
            book = rpc.call(
                'update_book',
                id, book_data.dict(), current_user.dict()
            )
        except HTTPException as http_exception:
            raise http_exception
        except Exception:
            _handle_non_http_exception()
        return Book.parse_obj(book)

    @app.delete(
        '/api/v1/books/{id}',
        response_model=Book
    )
    async def delete_book(
        id: str,
        current_user: Optional[User] = Depends(
            auth_service.has_permission('api:book:delete')
        )
    ) -> Book:
        '''
        Serving API to delete book by id.
        '''
        book = None
        try:
            current_user = _get_user_or_guest(current_user)
            book = rpc.call(
                'delete_book',
                id, current_user.dict()
            )
        except HTTPException as http_exception:
            raise http_exception
        except Exception:
            _handle_non_http_exception()
        return Book.parse_obj(book)

    def _handle_non_http_exception():
        '''
        Handle non HTTPException and return a default HTTPException
        '''
        logging.error('Non HTTPException error', exc_info=True)
        raise HTTPException(
            status_code=500,
            detail='Internal server serror'
        )

    def _get_user_or_guest(user: Optional[User]) -> User:
        '''
        If user is not set, this function will return guest_user
        '''
        if user is None:
            return User.parse_obj(auth_service.get_guest_user())
        return user

    logging.info(
        'Register library.book API route handler')


################################################
# -- 👓 User Interface
################################################
def register_book_ui_route(
    app: FastAPI,
    mb: AppMessageBus,
    rpc: AppRPC,
    menu_service: MenuService,
    page_template: Jinja2Templates
):

    # Book CRUD page
    menu_service.add_menu(
        name='library:books',
        title='Books',
        url='/library/books',
        auth_type=AuthType.HAS_PERMISSION,
        permission_name='ui:library:book',
        parent_name='library'
    )

    @app.get(
        '/library/books',
        response_class=HTMLResponse
    )
    async def manage_book(
        request: Request,
        context: MenuContext = Depends(
            menu_service.has_access('library:books')
        )
    ):
        '''
        Serving user interface for managing book.
        '''
        return page_template.TemplateResponse('default_crud.html', context={
            'content_path':
                'modules/library/crud/books.html',
            'request': request,
            'context': context
        }, status_code=200)

    logging.info(
        'Register library.book UI route handler')
