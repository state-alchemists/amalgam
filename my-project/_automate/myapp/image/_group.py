from zrb import Group

from .._group import myapp_group

myapp_image_group = Group(
    name="image",
    parent=myapp_group,
    description="Manage myapp images",
)
