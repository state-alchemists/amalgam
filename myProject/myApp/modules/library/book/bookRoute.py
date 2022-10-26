from typing import Any, List, Mapping, Optional
from helpers.transport import MessageBus, RPC
from fastapi import Depends, FastAPI, Request, HTTPException
from fastapi.security import OAuth2
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from core import AuthService, MenuService
from schemas.book import Book, BookData, BookResult
from schemas.menuContext import MenuContext
from schemas.user import User

import traceback
import sys

################################################
# -- ⚙️ API
################################################
def register_book_entity_api_route(app: FastAPI, mb: MessageBus, rpc: RPC, auth_service: AuthService):

    @app.get('/api/v1/books/', response_model=BookResult)
    async def find_books(keyword: str='', limit: int=100, offset: int=0, current_user: Optional[User] = Depends(auth_service.has_permission('api:book:read'))) -> BookResult:
        '''
        Serving API to find books by keyword.
        '''
        result = {}
        try:
            if not current_user:
                current_user = User.parse_obj(rpc.call('get_guest_user'))
            result = rpc.call('find_book', keyword, limit, offset, current_user.dict())
        except HTTPException as http_exception:
            raise http_exception
        except:
            print(traceback.format_exc(), file=sys.stderr) 
            raise HTTPException(status_code=500, detail='Internal Server Error')
        return BookResult.parse_obj(result)


    @app.get('/api/v1/books/{id}', response_model=Book)
    async def find_book_by_id(id: str, current_user: Optional[User] = Depends(auth_service.has_permission('api:book:read'))) -> Book:
        '''
        Serving API to find book by id.
        '''
        book = None
        try:
            if not current_user:
                current_user = User.parse_obj(rpc.call('get_guest_user'))
            book = rpc.call('find_book_by_id', id, current_user.dict())
        except HTTPException as http_exception:
            raise http_exception
        except:
            print(traceback.format_exc(), file=sys.stderr) 
            raise HTTPException(status_code=500, detail='Internal Server Error')
        return Book.parse_obj(book)


    @app.post('/api/v1/books/', response_model=Book)
    async def insert_book(book_data: BookData, current_user: Optional[User] = Depends(auth_service.has_permission('api:book:create'))) -> Book:
        '''
        Serving API to insert new book.
        '''
        book = None
        try:
            if not current_user:
                current_user = User.parse_obj(rpc.call('get_guest_user'))
            book = rpc.call('insert_book', book_data.dict(), current_user.dict())
        except HTTPException as http_exception:
            raise http_exception
        except:
            print(traceback.format_exc(), file=sys.stderr) 
            raise HTTPException(status_code=500, detail='Internal Server Error')
        return Book.parse_obj(book)


    @app.put('/api/v1/books/{id}', response_model=Book)
    async def update_book(id: str, book_data: BookData, current_user: Optional[User] = Depends(auth_service.has_permission('api:book:update'))) -> Book:
        '''
        Serving API to update book by id.
        '''
        book = None
        try:
            if not current_user:
                current_user = User.parse_obj(rpc.call('get_guest_user'))
            book = rpc.call('update_book', id, book_data.dict(), current_user.dict())
        except HTTPException as http_exception:
            raise http_exception
        except:
            print(traceback.format_exc(), file=sys.stderr) 
            raise HTTPException(status_code=500, detail='Internal Server Error')
        return Book.parse_obj(book)


    @app.delete('/api/v1/books/{id}')
    async def delete_book(id: str, current_user: Optional[User] = Depends(auth_service.has_permission('api:book:delete'))) -> Book:
        '''
        Serving API to delete book by id.
        '''
        book = None
        try:
            if not current_user:
                current_user = User.parse_obj(rpc.call('get_guest_user'))
            book = rpc.call('delete_book', id, current_user.dict())
        except HTTPException as http_exception:
            raise http_exception
        except:
            print(traceback.format_exc(), file=sys.stderr) 
            raise HTTPException(status_code=500, detail='Internal Server Error')
        return Book.parse_obj(book)


################################################
# -- 👓 User Interface
################################################
def register_book_entity_ui_route(app: FastAPI, mb: MessageBus, rpc: RPC, menu_service: MenuService, page_template: Jinja2Templates):

    @app.get('/library/books', response_class=HTMLResponse)
    async def manage_book(request: Request, context: MenuContext = Depends(menu_service.has_access('library:books'))):
        '''
        Serving user interface for managing book.
        '''
        return page_template.TemplateResponse('default_crud.html', context={
            'api_path': '/api/vi/ztp_app_crud_entities',
            'content_path': 'library/crud/books.html',
            'request': request, 
            'context': context
        }, status_code=200)
