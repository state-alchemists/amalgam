from passlib.context import CryptContext

from myapp.common.base_db_repository import BaseDBRepository
from myapp.module.my_module.service.my_entity.repository.my_entity_repository import (
    MyEntityRepository,
)
from myapp.schema.my_entity import (
    MyEntity,
    MyEntityCreateWithAudit,
    MyEntityResponse,
    MyEntityUpdateWithAudit,
)


class MyEntityDBRepository(
    BaseDBRepository[
        MyEntity,
        MyEntityResponse,
        MyEntityCreateWithAudit,
        MyEntityUpdateWithAudit,
    ],
    MyEntityRepository,
):
    db_model = MyEntity
    response_model = MyEntityResponse
    create_model = MyEntityCreateWithAudit
    update_model = MyEntityUpdateWithAudit
    entity_name = "my_entity"
    column_preprocessors = {}
