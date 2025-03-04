from sqlalchemy import MetaData

from myapp.schema.permission import Permission
from myapp.schema.role import Role, RolePermission
from myapp.schema.user import User, UserRole, UserSession

metadata = MetaData()

Permission.metadata = metadata
Permission.__table__.tometadata(metadata)

Role.metadata = metadata
Role.__table__.tometadata(metadata)
RolePermission.metadata = metadata
RolePermission.__table__.tometadata(metadata)

User.metadata = metadata
User.__table__.tometadata(metadata)
UserRole.metadata = metadata
UserRole.__table__.tometadata(metadata)

UserSession.metadata = metadata
UserSession.__table__.tometadata(metadata)
