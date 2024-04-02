from ._group import myapp_group
from .backend import (
    prepare_myapp_backend,
    myapp_backend_group,
)
from .container import (
    remove_myapp_container,
    myapp_container_group,
    myapp_microservices_container_group,
    myapp_monolith_container_group,
    myapp_support_container_group,
    start_myapp_microservices_container,
    start_myapp_monolith_container,
    start_myapp_support_container,
    stop_myapp_container,
)
from .destroy import destroy_myapp
from .frontend import (
    build_myapp_frontend,
    build_myapp_frontend_once,
    myapp_frontend_group,
)
from .image import (
    build_myapp_image,
    push_myapp_image,
    myapp_image_group,
)
from .load_test import load_test_myapp
from .microservices import (
    deploy_myapp_microservices,
    myapp_microservices_group,
    start_myapp_microservices,
)
from .monolith import (
    deploy_myapp_monolith,
    myapp_monolith_group,
    start_myapp_monolith,
)
from .test import test_myapp

assert myapp_group
assert myapp_backend_group
assert myapp_frontend_group
assert myapp_microservices_group
assert myapp_monolith_group
assert myapp_image_group
assert myapp_container_group
assert myapp_microservices_container_group
assert myapp_monolith_container_group
assert myapp_support_container_group
assert destroy_myapp
assert start_myapp_microservices
assert deploy_myapp_microservices
assert start_myapp_monolith
assert deploy_myapp_monolith
assert remove_myapp_container
assert stop_myapp_container
assert start_myapp_microservices_container
assert start_myapp_monolith_container
assert start_myapp_support_container
assert build_myapp_image
assert push_myapp_image
assert build_myapp_frontend_once
assert build_myapp_frontend
assert prepare_myapp_backend
assert load_test_myapp
assert test_myapp
