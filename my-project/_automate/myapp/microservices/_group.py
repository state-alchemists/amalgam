from zrb import Group

from .._group import myapp_group

myapp_microservices_group = Group(
    name="microservices",
    parent=myapp_group,
    description="Manage myapp as microservices",
)
