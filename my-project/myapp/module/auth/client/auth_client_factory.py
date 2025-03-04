from myapp.config import APP_COMMUNICATION
from myapp.module.auth.client.auth_api_client import AuthAPIClient
from myapp.module.auth.client.auth_client import AuthClient
from myapp.module.auth.client.auth_direct_client import AuthDirectClient

if APP_COMMUNICATION == "direct":
    auth_client: AuthClient = AuthDirectClient()
elif APP_COMMUNICATION == "api":
    auth_client: AuthClient = AuthAPIClient()
