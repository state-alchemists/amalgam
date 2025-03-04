from myapp.common.app_factory import app
from myapp.module.auth import route as auth_route
from myapp.module.gateway import route as gateway_route
from myapp.module.library import route as library_route

assert app
assert gateway_route
assert auth_route


assert library_route
