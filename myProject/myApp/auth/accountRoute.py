from typing import Any, List, Mapping
from helpers.transport import MessageBus, RPC
from fastapi import Depends, FastAPI, Request, HTTPException
from fastapi.security import OAuth2
from auth.authService import AuthService
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from schemas.menuContext import MenuContext
from ui.menuService import MenuService

import traceback

class CreateAccessTokenRequest(BaseModel):
    username: str
    password: str

class CreateAccessTokenResponse(BaseModel):
    access_token: str
    token_type: str

class RefreshAccessTokenRequest(BaseModel):
    access_token: str

class RefreshAccessTokenResponse(BaseModel):
    access_token: str
    token_type: str


def register_account_route(app: FastAPI, mb: MessageBus, rpc: RPC, menu_service: MenuService, templates: Jinja2Templates, enable_ui: bool, enable_api: bool, create_oauth_access_token_url: str, create_access_token_url: str, refresh_access_token_url: str):

    ################################################
    # -- ⚙️ API
    ################################################
    if enable_api:

        @app.post(create_oauth_access_token_url, response_model=CreateAccessTokenResponse)
        async def create_oauth_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
            try:
                username = form_data.username
                password = form_data.password
                access_token = rpc.call('create_access_token', username, password)
                return CreateAccessTokenResponse(access_token = access_token, token_type = 'bearer')
            except:
                print(traceback.format_exc()) 
                raise HTTPException(status_code=400, detail='Incorrect identity or password')

        @app.post(create_access_token_url, response_model=CreateAccessTokenResponse)
        async def create_access_token(data: CreateAccessTokenRequest):
            try:
                username = data.username
                password = data.password
                access_token = rpc.call('create_access_token', username, password)
                return CreateAccessTokenResponse(access_token = access_token, token_type = 'bearer')
            except:
                print(traceback.format_exc()) 
                raise HTTPException(status_code=400, detail='Incorrect identity or password')

        @app.post(refresh_access_token_url, response_model=RefreshAccessTokenResponse)
        async def refresh_access_token(data: RefreshAccessTokenRequest):
            try:
                old_access_token = data.access_token
                new_access_token = rpc.call('refresh_access_token', old_access_token)
                return RefreshAccessTokenResponse(access_token = new_access_token, token_type = 'bearer')
            except:
                print(traceback.format_exc()) 
                raise HTTPException(status_code=400, detail='Incorrect identity or password')
    

    ################################################
    # -- 👓 User Interface
    ################################################
    if enable_ui:

        @app.get('/account/login', response_class=HTMLResponse)
        async def user_interface(request: Request, context: MenuContext = Depends(menu_service.authenticate('account/login'))):
            return templates.TemplateResponse(
                'default_login.html', 
                context={
                    'request': request, 
                    'context': context,
                    'create_access_token_url': create_access_token_url
                }, 
                status_code=200
            )

        @app.get('/account/logout', response_class=HTMLResponse)
        async def user_interface(request: Request, context: MenuContext = Depends(menu_service.authenticate('account/logout'))):
            return templates.TemplateResponse(
                'default_logout.html', 
                context={
                    'request': request, 
                    'context': context,
                }, 
                status_code=200
            )


