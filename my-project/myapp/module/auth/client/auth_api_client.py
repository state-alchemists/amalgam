from myapp.config import APP_AUTH_BASE_URL
from myapp.module.auth.client.auth_client import AuthClient
from myapp.module.auth.service.permission.permission_service_factory import (
    permission_service,
)
from myapp.module.auth.service.role.role_service_factory import role_service
from myapp.module.auth.service.user.user_service_factory import user_service


class AuthAPIClient(
    permission_service.as_api_client(base_url=APP_AUTH_BASE_URL),
    role_service.as_api_client(base_url=APP_AUTH_BASE_URL),
    user_service.as_api_client(base_url=APP_AUTH_BASE_URL),
    AuthClient,
):
    pass
