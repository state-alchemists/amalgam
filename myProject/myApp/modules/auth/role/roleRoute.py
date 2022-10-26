from typing import Any, List, Mapping, Optional
from helpers.transport import MessageBus, RPC
from fastapi import Depends, FastAPI, Request, HTTPException
from fastapi.security import OAuth2
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from core import AuthService, MenuService
from schemas.menuContext import MenuContext
from schemas.role import Role, RoleData, RoleResult
from schemas.user import User
 
import traceback
import sys

################################################
# -- ⚙️ API
################################################
def register_role_api_route(app: FastAPI, mb: MessageBus, rpc: RPC, auth_service: AuthService):

    @app.get('/api/v1/roles/', response_model=RoleResult)
    def find_roles(keyword: str='', limit: int=100, offset: int=0, current_user: Optional[User] = Depends(auth_service.has_permission('api:role:read'))) -> RoleResult:
        '''
        Serving API to find roles by keyword.
        '''
        result = {}
        try:
            if not current_user:
                current_user = User.parse_obj(rpc.call('get_guest_user'))
            result = rpc.call('find_roles', keyword, limit, offset, current_user.dict())
        except HTTPException as http_exception:
            raise http_exception
        except:
            print(traceback.format_exc(), file=sys.stderr) 
            raise HTTPException(status_code=500, detail='Internal Server Error')
        return RoleResult.parse_obj(result)


    @app.get('/api/v1/roles/{id}', response_model=Role)
    def find_role_by_id(id: str, current_user: Optional[User] = Depends(auth_service.has_permission('api:role:read'))) -> Role:
        '''
        Serving API to find role by id.
        '''
        result = None
        try:
            if not current_user:
                current_user = User.parse_obj(rpc.call('get_guest_user'))
            result = rpc.call('find_role_by_id', id, current_user.dict())
        except HTTPException as http_exception:
            raise http_exception
        except:
            print(traceback.format_exc(), file=sys.stderr) 
            raise HTTPException(status_code=500, detail='Internal Server Error')
        return Role.parse_obj(result)


    @app.post('/api/v1/roles/', response_model=Role)
    def insert_role(role_data: RoleData, current_user: Optional[User] = Depends(auth_service.has_permission('api:role:create'))) -> Role:
        '''
        Serving API to insert new role.
        '''
        result = None
        try:
            if not current_user:
                current_user = User.parse_obj(rpc.call('get_guest_user'))
            result = rpc.call('insert_role', role_data.dict(), current_user.dict())
        except HTTPException as http_exception:
            raise http_exception
        except:
            print(traceback.format_exc(), file=sys.stderr) 
            raise HTTPException(status_code=500, detail='Internal Server Error')
        return Role.parse_obj(result)


    @app.put('/api/v1/roles/{id}', response_model=Role)
    def update_role(id: str, role_data: RoleData, current_user: Optional[User] = Depends(auth_service.has_permission('api:role:update'))) -> Role:
        '''
        Serving API to update role by id.
        '''
        result = None
        try:
            if not current_user:
                current_user = User.parse_obj(rpc.call('get_guest_user'))
            result = rpc.call('update_role', id, role_data.dict(), current_user.dict())
        except HTTPException as http_exception:
            raise http_exception
        except:
            print(traceback.format_exc(), file=sys.stderr) 
            raise HTTPException(status_code=500, detail='Internal Server Error')
        return Role.parse_obj(result)


    @app.delete('/api/v1/roles/{id}')
    def delete_role(id: str, current_user: Optional[User] = Depends(auth_service.has_permission('api:role:delete'))) -> Role:
        '''
        Serving API to delete role by id.
        '''
        result = None
        try:
            if not current_user:
                current_user = User.parse_obj(rpc.call('get_guest_user'))
            result = rpc.call('delete_role', id, current_user.dict())
        except HTTPException as http_exception:
            raise http_exception
        except:
            print(traceback.format_exc(), file=sys.stderr) 
            raise HTTPException(status_code=500, detail='Internal Server Error')
        return Role.parse_obj(result)


################################################
# -- 👓 User Interface
################################################
def register_role_ui_route(app: FastAPI, mb: MessageBus, rpc: RPC, menu_service: MenuService, page_template: Jinja2Templates):

    @app.get('/auth/roles', response_class=HTMLResponse)
    async def manage_role(request: Request, context: MenuContext = Depends(menu_service.has_access('auth:roles'))):
        '''
        Serving user interface to manage role.
        '''
        return page_template.TemplateResponse('default_crud.html', context={
            'api_path': '/api/vi/roles',
            'content_path': 'auth/crud/roles.html',
            'request': request, 
            'context': context
        }, status_code=200)
