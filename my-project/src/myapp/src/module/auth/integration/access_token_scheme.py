from config import APP_AUTH_ACCESS_TOKEN_COOKIE_KEY
from module.auth.component import (
    AccessTokenScheme,
    create_oauth2_bearer_access_token_scheme,
)
from module.auth.integration.access_token_util import access_token_util
from module.auth.integration.user import guest_user

access_token_scheme: AccessTokenScheme = (
    create_oauth2_bearer_access_token_scheme(  # noqa
        guest_user=guest_user,
        access_token_util=access_token_util,
        token_url="/api/v1/auth/login-oauth",
        token_cookie_key=APP_AUTH_ACCESS_TOKEN_COOKIE_KEY,
    )
)
