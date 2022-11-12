from modules.library.book import register_book_api_route, register_book_ui_route
from typing import Mapping, List, Any, Optional
from fastapi import Depends, FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from core import AuthService, MenuService
from transport import AppMessageBus, AppRPC
from schemas.menuContext import MenuContext
from schemas.user import User
from schemas.authType import AuthType

import traceback
import sys


################################################
# -- ⚙️ API
################################################
# Note: 💀 Don't delete the following line, Zaruba use it for pattern matching
def register_library_api_route(app: FastAPI, mb: AppMessageBus, rpc: AppRPC, auth_service: AuthService):

    register_book_api_route(app, mb, rpc, auth_service)

    print('Register library api route handler', file=sys.stderr)


################################################
# -- 👓 User Interface
################################################
# Note: 💀 Don't delete the following line, Zaruba use it for pattern matching
def register_library_ui_route(app: FastAPI, mb: AppMessageBus, rpc: AppRPC, menu_service: MenuService, page_template: Jinja2Templates):

    # Note: 💀 Don't delete the following line, Zaruba use it for pattern matching
    menu_service.add_menu(name='library', title='Library', url='#', auth_type=AuthType.ANYONE)
    # register menu
    menu_service.add_menu(name='library:/about', title='About', url='/about', auth_type=AuthType.ANYONE, parent_name='library')

    @app.get('/about', response_class=HTMLResponse)
    async def get_about(request: Request, context: MenuContext = Depends(menu_service.has_access('library:/about'))) -> HTMLResponse:
        '''
        Serve (get) /about
        '''
        try:
            return page_template.TemplateResponse('default_page.html', context={
                'request': request,
                'context': context,
                'content_path': 'modules/library/about.html'
            }, status_code=200)
        except:
            print(traceback.format_exc(), file=sys.stderr) 
            return page_template.TemplateResponse('default_error.html', context={
                'request': request,
                'status_code': 500,
                'detail': 'Internal server error'
            }, status_code=500)

    register_book_ui_route(app, mb, rpc, menu_service, page_template)

    print('Register library UI route handler', file=sys.stderr)