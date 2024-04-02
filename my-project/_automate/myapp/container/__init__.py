from ._group import myapp_container_group
from .microservices import (
    myapp_microservices_container_group,
    start_myapp_microservices_container,
)
from .monolith import (
    myapp_monolith_container_group,
    start_myapp_monolith_container,
)
from .remove import remove_myapp_container
from .stop import stop_myapp_container
from .support import (
    myapp_support_container_group,
    start_myapp_support_container,
)

assert myapp_container_group
assert myapp_microservices_container_group
assert myapp_monolith_container_group
assert myapp_support_container_group
assert start_myapp_microservices_container
assert start_myapp_monolith_container
assert start_myapp_support_container
assert remove_myapp_container
assert stop_myapp_container
