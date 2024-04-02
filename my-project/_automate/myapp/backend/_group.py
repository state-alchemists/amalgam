from zrb import Group

from .._group import myapp_group

myapp_backend_group = Group(
    name="backend",
    parent=myapp_group,
    description="Manage myapp backend",
)
