from zrb import Group

from .._group import myapp_group

myapp_frontend_group = Group(
    name="frontend",
    parent=myapp_group,
    description="Manage myapp frontend",
)
