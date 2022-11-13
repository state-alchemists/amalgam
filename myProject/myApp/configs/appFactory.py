from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
from core import MenuService, PageTemplateException
from helpers.transport import MessageBus, RPC
from configs.cors import cors_allow_credentials, cors_allow_headers, cors_allow_methods, cors_allow_origin_regex, cors_allow_origins, cors_expose_headers, cors_max_age
from configs.dir import public_dir
from configs.error import error_threshold
from configs.ui import site_name
from configs.featureFlag import enable_error_page, enable_ui
from configs.url import public_url_path 
from schemas.menuContext import MenuContext
from schemas.authType import AuthType

import re
import sys
import traceback

def create_app(mb: MessageBus, rpc: RPC, menu_service: MenuService, page_template: Jinja2Templates) -> FastAPI:
    app = FastAPI(title=site_name)


    # 🔀 Apply CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins = cors_allow_origins,
        allow_origin_regex = cors_allow_origin_regex,
        allow_methods = cors_allow_methods,
        allow_headers = cors_allow_headers,
        allow_credentials = cors_allow_credentials,
        expose_headers = cors_expose_headers,
        max_age = cors_max_age,
    )


    # 🥑 Handle readiness request
    @app.get('/readiness')
    def handle_readiness():
        if mb.is_failing():
            raise HTTPException(status_code=500, detail='messagebus is failing')
        if rpc.is_failing():
            raise HTTPException(status_code=500, detail='RPC is failing')
        if mb.get_error_count() > error_threshold:
            raise HTTPException(status_code=500, detail='messagebus error exceeding threshold')
        if rpc.get_error_count() > error_threshold:
            raise HTTPException(status_code=500, detail='RPC error exceeding threshold')
        return HTMLResponse(content='ready', status_code=200)


    # 🔚 Handle application shutdown
    @app.on_event('shutdown')
    def on_shutdown():
        mb.shutdown()
        rpc.shutdown()
    print('Register app shutdown handler', file=sys.stderr)


    # 📢 serve public static directory (js, css, html, images, etc)
    if public_dir != '':
        app.mount(public_url_path, StaticFiles(directory=public_dir), name='static-resources')
        print('Register static directory route', file=sys.stderr)


    # 🏠 Serve home page 
    if enable_ui:
        menu_service.add_menu(name='home', title='Home', url='/', auth_type=AuthType.ANYONE)
        @app.get('/', response_class=HTMLResponse)
        async def get_home(request: Request, context: MenuContext = Depends(menu_service.has_access('home'))) -> HTMLResponse:
            '''
            Handle (get) /
            '''
            try:
                return page_template.TemplateResponse('default_page.html', context={
                    'request': request,
                    'context': context,
                    'content_path': 'home.html'
                }, status_code=200)
            except:
                print(traceback.format_exc(), file=sys.stderr) 
                return page_template.TemplateResponse('default_error.html', context={
                    'request': request,
                    'status_code': 500,
                    'detail': 'Internal server error'
                }, status_code=500)


    # ❌ Handle any PageTemplateException 
    if enable_ui and enable_error_page:
        @app.exception_handler(PageTemplateException)
        def handle_template_exception(request: Request, exception: PageTemplateException):
            menu_context = exception.menu_context
            return page_template.TemplateResponse(
                'default_error.html',
                context={
                    'request': request,
                    'status_code': exception.status_code,
                    'detail': exception.detail, 
                    'context': menu_context
                },
                status_code=exception.status_code
            )

    # ❌ Handle any StarletteHTTPException
    if enable_ui and enable_error_page:
        @app.exception_handler(StarletteHTTPException)
        def handle_template_exception(request: Request, exception: StarletteHTTPException):
            url = request.url.path
            if re.search("\/api\/", url):
                # Do not override error generated by /api/
                return JSONResponse(content={'detail': exception.detail}, status_code=exception.status_code)
            return page_template.TemplateResponse(
                'default_error.html',
                context={
                    'request': request,
                    'status_code': exception.status_code,
                    'detail': exception.detail, 
                    'context': None
                },
                status_code=exception.status_code
            )

    return app