from zrb import Group

from .._group import myapp_container_group

myapp_monolith_container_group = Group(
    name="monolith",
    parent=myapp_container_group,
    description="Manage myapp monolith containers",
)
