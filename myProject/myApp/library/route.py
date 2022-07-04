from library.bookRoute import register_book_route
from typing import Mapping, List, Any
from fastapi import Depends, FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from schemas.menuContext import MenuContext
from schemas.user import User
from auth.authService import AuthService
from ui.menuService import MenuService
from helpers.transport import MessageBus, RPC

import traceback

def register_library_route_handler(app: FastAPI, mb: MessageBus, rpc: RPC, auth_service: AuthService, menu_service: MenuService, templates: Jinja2Templates, enable_ui: bool, enable_api:bool):

    if enable_ui:
        @app.get('/', response_class=HTMLResponse)
        async def get_(request: Request, context: MenuContext = Depends(menu_service.authenticate('library:/'))) -> HTMLResponse:
            '''
            Handle (get) /
            '''
            try:
                return templates.TemplateResponse('default_page.html', context={
                    'request': request,
                    'context': context,
                    'content_path': 'library/.html'
                }, status_code=200)
            except:
                print(traceback.format_exc()) 
                return templates.TemplateResponse('default_error.html', context={
                    'request': request,
                    'status_code': 500,
                    'detail': 'Internal server error'
                }, status_code=500)

    register_book_route(app, mb, rpc, auth_service, menu_service, templates, enable_ui, enable_api)
    # NOTE: follow [this](https://fastapi.tiangolo.com/tutorial/security/first-steps/#how-it-looks) guide for authorization

    print('Register library route handler')