from zrb import Group

from .._group import myapp_container_group

myapp_support_container_group = Group(
    name="support",
    parent=myapp_container_group,
    description="Manage myapp support containers",
)
