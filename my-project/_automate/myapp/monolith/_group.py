from zrb import Group

from .._group import myapp_group

myapp_monolith_group = Group(
    name="monolith",
    parent=myapp_group,
    description="Manage myapp as monolith",
)
