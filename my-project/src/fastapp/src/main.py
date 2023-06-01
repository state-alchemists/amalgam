from component.app import app
from module.auth.register_module import register_auth
from module.log.register_module import register_log
from module.library.register_module import register_library

# Make sure app is loaded.
# Uvicorn or adny ASGII server you use will pick it up and run the app.
assert app
register_auth()
register_log()
register_library()
