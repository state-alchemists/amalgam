from modules.library.book import register_book_api_route, register_book_ui_route
from typing import Mapping, List, Any, Optional
from fastapi import Depends, FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from core import AuthService, MenuService
from helpers.transport import MessageBus, RPC
from schemas.menuContext import MenuContext
from schemas.user import User

import traceback
import sys


################################################
# -- ⚙️ API
################################################
# Note: 💀 Don't delete the following line, Zaruba use it for pattern matching
def register_library_api_route(app: FastAPI, mb: MessageBus, rpc: RPC, auth_service: AuthService):

    register_book_api_route(app, mb, rpc, auth_service)

    print('Register library api route handler', file=sys.stderr)


################################################
# -- 👓 User Interface
################################################
# Note: 💀 Don't delete the following line, Zaruba use it for pattern matching
def register_library_ui_route(app: FastAPI, mb: MessageBus, rpc: RPC, menu_service: MenuService, page_template: Jinja2Templates):

    @app.get('/', response_class=HTMLResponse)
    async def get_(request: Request, context: MenuContext = Depends(menu_service.has_access('library:/'))) -> HTMLResponse:
        '''
        Handle (get) /
        '''
        try:
            return page_template.TemplateResponse('default_page.html', context={
                'request': request,
                'context': context,
                'content_path': 'modules/library/.html'
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