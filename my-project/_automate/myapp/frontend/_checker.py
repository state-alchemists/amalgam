from zrb import PathChecker

from .._constant import APP_FRONTEND_BUILD_DIR
from ._group import myapp_frontend_group

check_frontend_path = PathChecker(
    name="check-frontend-path",
    group=myapp_frontend_group,
    path=APP_FRONTEND_BUILD_DIR,
)
