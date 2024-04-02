from zrb import Group

from .._group import myapp_group

myapp_container_group = Group(
    name="container",
    parent=myapp_group,
    description="Manage myapp containers",
)
