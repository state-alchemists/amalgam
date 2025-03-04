from myapp.common.logger_factory import logger
from myapp.module.auth.service.permission.permission_service import PermissionService
from myapp.module.auth.service.permission.repository.permission_repository_factory import (
    permission_repository,
)

permission_service = PermissionService(
    logger, permission_repository=permission_repository
)
