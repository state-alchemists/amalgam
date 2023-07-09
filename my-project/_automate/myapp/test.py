from zrb import CmdTask, StrInput, Env, EnvFile, runner, python_task
from zrb.builtin._group import project_group
from ._common import (
    CURRENT_DIR, RESOURCE_DIR, APP_TEMPLATE_ENV_FILE_NAME,
)
from .frontend import build_myapp_frontend_once
from .local import prepare_myapp_backend
import os

###############################################################################
# Env file Definitions
###############################################################################

app_env_file = EnvFile(
    env_file=APP_TEMPLATE_ENV_FILE_NAME, prefix='TEST_MYAPP'
)

###############################################################################
# Task Definitions
###############################################################################


@python_task(
    icon='🧪',
    name='remove-myapp-test-db',
    group=project_group,
    runner=runner
)
def remove_myapp_test_db(*args, **kwargs):
    test_db_file_path = os.path.join(RESOURCE_DIR, 'test.db')
    if os.path.isfile(test_db_file_path):
        os.remove(test_db_file_path)


test_myapp = CmdTask(
    icon='🚤',
    name='test-myapp',
    group=project_group,
    inputs=[
        StrInput(
            name='myapp-test',
            description='Specific test case (i.e., test/file.py::test_name)',
            prompt='Test (i.e., test/file.py::test_name)',
            default=''
        )
    ],
    upstreams=[
        build_myapp_frontend_once,
        prepare_myapp_backend,
        remove_myapp_test_db,
    ],
    cwd=RESOURCE_DIR,
    env_files=[app_env_file],
    envs=[
        Env(
            name='APP_BROKER_TYPE',
            os_name='TEST_APP_BROKER_TYPE',
            default='mock'
        ),
        Env(
            name='APP_DB_CONNECTION',
            os_name='TEST_APP_DB_CONNECTION',
            default='sqlite:///test.db'
        ),
        Env(
            name='APP_AUTH_ADMIN_ACTIVE',
            os_name='',
            default='true'
        ),
        Env(
            name='APP',
            os_name='APP_ENABLE_OTEL',
            default='false'
        ),
    ],
    cmd_path=os.path.join(CURRENT_DIR, 'cmd', 'test.sh'),
    retry=0
)
runner.register(test_myapp)
