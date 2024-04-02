from zrb import Group

from .._group import myapp_container_group

myapp_microservices_container_group = Group(
    name="microservices",
    parent=myapp_container_group,
    description="Manage myapp microservices containers",
)
