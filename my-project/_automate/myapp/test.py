import os

from zrb import CmdTask, Env, EnvFile, StrInput, python_task, runner

from ._constant import APP_TEMPLATE_ENV_FILE_NAME, RESOURCE_DIR
from ._group import myapp_group
from .backend import prepare_myapp_backend
from .frontend import build_myapp_frontend_once

CURRENT_DIR = os.path.dirname(__file__)


@python_task(
    icon="🧪",
    name="remove-test-db",
    group=myapp_group,
    runner=runner,
)
def remove_myapp_test_db(*args, **kwargs):
    test_db_file_path = os.path.join(RESOURCE_DIR, "test.db")
    if os.path.isfile(test_db_file_path):
        os.remove(test_db_file_path)


test_myapp = CmdTask(
    icon="🚤",
    name="test",
    group=myapp_group,
    inputs=[
        StrInput(
            name="myapp-test",
            description="Specific test case (i.e., test/file.py::test_name)",
            prompt="Test (i.e., test/file.py::test_name)",
            default="",
        )
    ],
    upstreams=[
        build_myapp_frontend_once,
        prepare_myapp_backend,
        remove_myapp_test_db,
    ],
    cwd=RESOURCE_DIR,
    env_files=[EnvFile(path=APP_TEMPLATE_ENV_FILE_NAME, prefix="TEST_MYAPP")],
    envs=[
        Env(name="APP_BROKER_TYPE", os_name="TEST_APP_BROKER_TYPE", default="mock"),
        Env(
            name="APP_DB_CONNECTION",
            os_name="TEST_APP_DB_CONNECTION",
            default="sqlite:///test.db",
        ),
        Env(name="APP_AUTH_ADMIN_ACTIVE", os_name="", default="true"),
        Env(name="APP", os_name="APP_ENABLE_OTEL", default="false"),
    ],
    cmd_path=os.path.join(CURRENT_DIR, "test.sh"),
    retry=0,
)
runner.register(test_myapp)
