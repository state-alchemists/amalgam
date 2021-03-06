from typing import Any, List, Mapping
from helpers.transport import MessageBus, RPC
from fastapi import Depends, FastAPI, Request, HTTPException
from fastapi.security import OAuth2
from auth.authService import AuthService
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from ui.menuService import MenuService
from schemas.book import Book, BookData, BookResult
from schemas.menuContext import MenuContext
from schemas.user import User

import traceback

def register_book_route(app: FastAPI, mb: MessageBus, rpc: RPC, auth_service: AuthService, menu_service: MenuService, templates: Jinja2Templates, enable_ui: bool, enable_api:bool):

    ################################################
    # -- ⚙️ API
    ################################################
    if enable_api:

        @app.get('/api/v1/books/', response_model=BookResult)
        def find_books(keyword: str='', limit: int=100, offset: int=0, current_user:  User = Depends(auth_service.is_authorized('api:book:read'))) -> BookResult:
            result = {}
            try:
                result = rpc.call('find_book', keyword, limit, offset)
            except:
                print(traceback.format_exc()) 
                raise HTTPException(status_code=500, detail='Internal Server Error')
            return BookResult.parse_obj(result)


        @app.get('/api/v1/books/{id}', response_model=Book)
        def find_book_by_id(id: str, current_user:  User = Depends(auth_service.is_authorized('api:book:read'))) -> Book:
            book = None
            try:
                book = rpc.call('find_book_by_id', id)
            except:
                print(traceback.format_exc()) 
                raise HTTPException(status_code=500, detail='Internal Server Error')
            if book is None:
                raise HTTPException(status_code=404, detail='Not Found')
            return Book.parse_obj(book)


        @app.post('/api/v1/books/', response_model=Book)
        def insert_book(book_data: BookData, current_user:  User = Depends(auth_service.is_authorized('api:book:create'))) -> Book:
            book = None
            try:
                book = rpc.call('insert_book', book_data.dict(), current_user.dict())
            except:
                print(traceback.format_exc()) 
                raise HTTPException(status_code=500, detail='Internal Server Error')
            if book is None:
                raise HTTPException(status_code=404, detail='Not Found')
            return Book.parse_obj(book)


        @app.put('/api/v1/books/{id}', response_model=Book)
        def update_book(id: str, book_data: BookData, current_user:  User = Depends(auth_service.is_authorized('api:book:update'))) -> Book:
            book = None
            try:
                book = rpc.call('update_book', id, book_data.dict(), current_user.dict())
            except:
                print(traceback.format_exc()) 
                raise HTTPException(status_code=500, detail='Internal Server Error')
            if book is None:
                raise HTTPException(status_code=404, detail='Not Found')
            return Book.parse_obj(book)


        @app.delete('/api/v1/books/{id}')
        def delete_book(id: str, current_user:  User = Depends(auth_service.is_authorized('api:book:delete'))) -> Book:
            book = None
            try:
                book = rpc.call('delete_book', id, current_user.dict())
            except:
                print(traceback.format_exc()) 
                raise HTTPException(status_code=500, detail='Internal Server Error')
            if book is None:
                raise HTTPException(status_code=404, detail='Not Found')
            return Book.parse_obj(book)


    ################################################
    # -- 👓 User Interface
    ################################################
    if enable_ui:

        @app.get('/library/books', response_class=HTMLResponse)
        async def user_interface(request: Request, context: MenuContext = Depends(menu_service.authenticate('library:books'))):
            return templates.TemplateResponse('default_crud.html', context={
                'api_path': '/api/vi/ztp_app_crud_entities',
                'content_path': 'library/crud/books.html',
                'request': request, 
                'context': context
            }, status_code=200)

    print('Handle HTTP routes for library.Book')