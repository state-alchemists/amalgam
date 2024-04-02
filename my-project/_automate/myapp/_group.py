from zrb import Group
from zrb.builtin import project_group

myapp_group = Group(
    name="myapp",
    parent=project_group,
    description="Manage myapp",
)
