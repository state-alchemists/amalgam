from myapp.common.logger_factory import logger
from myapp.module.auth.service.role.repository.role_repository_factory import (
    role_repository,
)
from myapp.module.auth.service.role.role_service import RoleService

role_service = RoleService(logger, role_repository=role_repository)
