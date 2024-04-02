from ._group import myapp_image_group
from .build import build_myapp_image
from .push import push_myapp_image

assert myapp_image_group
assert build_myapp_image
assert push_myapp_image
