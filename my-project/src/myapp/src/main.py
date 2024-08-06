from integration.app.app import app
from module.auth.register_module import register_auth
from module.log.register_module import register_log
from module.library.register_module import register_library

assert app
register_auth()
register_log()
register_library()
