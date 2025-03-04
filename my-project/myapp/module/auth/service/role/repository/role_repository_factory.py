from myapp.common.db_engine_factory import db_engine
from myapp.config import APP_REPOSITORY_TYPE
from myapp.module.auth.service.role.repository.role_db_repository import (
    RoleDBRepository,
)
from myapp.module.auth.service.role.repository.role_repository import RoleRepository

if APP_REPOSITORY_TYPE == "db":
    role_repository: RoleRepository = RoleDBRepository(db_engine)
else:
    role_repository: RoleRepository = None
