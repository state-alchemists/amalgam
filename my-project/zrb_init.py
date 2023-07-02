import _automate._project as _project
import _automate.myapp.local as myapp_local
import _automate.myapp.container as myapp_container
import _automate.myapp.image as myapp_image
import _automate.myapp.deployment as myapp_deployment
import _automate.myapp.test as myapp_test
import _automate.myapp.load_test as myapp_load_test
assert _project
assert myapp_local
assert myapp_container
assert myapp_image
assert myapp_deployment
assert myapp_test
assert myapp_load_test
