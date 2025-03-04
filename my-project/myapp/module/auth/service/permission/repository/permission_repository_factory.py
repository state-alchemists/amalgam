from myapp.common.db_engine_factory import db_engine
from myapp.config import APP_REPOSITORY_TYPE
from myapp.module.auth.service.permission.repository.permission_db_repository import (
    PermissionDBRepository,
)
from myapp.module.auth.service.permission.repository.permission_repository import (
    PermissionRepository,
)

if APP_REPOSITORY_TYPE == "db":
    permission_repository: PermissionRepository = PermissionDBRepository(db_engine)
else:
    permission_repository: PermissionRepository = None
