import os

from zrb import BoolInput, CmdTask, EnvFile, IntInput, StrInput, runner

from ._constant import LOAD_TEST_DIR, LOAD_TEST_TEMPLATE_ENV_FILE_NAME
from ._group import myapp_group

_CURRENT_DIR = os.path.dirname(__file__)

prepare_myapp_load_test = CmdTask(
    icon="🚤",
    name="prepare-load-test",
    description="Prepare load test for myapp",
    group=myapp_group,
    cwd=LOAD_TEST_DIR,
    cmd_path=[
        os.path.join(_CURRENT_DIR, "cmd", "activate-venv.sh"),
        os.path.join(_CURRENT_DIR, "cmd", "app-prepare-load-test.sh"),
    ],
)
runner.register(prepare_myapp_load_test)


load_test_myapp = CmdTask(
    icon="🧪",
    name="load-test",
    description="Load test myapp",
    group=myapp_group,
    upstreams=[prepare_myapp_load_test],
    inputs=[
        BoolInput(
            name="myapp-load-test-headless",
            default=True,
            description="Load test UI headless",
            prompt="Load test UI headless (if True, there will be no UI)",
        ),
        IntInput(
            name="myapp-load-test-port",
            default=8089,
            description="Load test UI web port",
            prompt="Load test UI web port (Only works if headless is False)",
        ),
        IntInput(
            name="myapp-load-test-users",
            default=200,
            description="Load test users",
            prompt="Load test users",
        ),
        IntInput(
            name="myapp-load-test-spawn-rate",
            default=10,
            description="Load test spawn rate",
            prompt="Load test spawn rate",
        ),
        StrInput(
            name="myapp-load-test-url",
            default="http://localhost:3000",
            description="Load test url",
            prompt="Load test url",
        ),
    ],
    cwd=LOAD_TEST_DIR,
    env_files=[
        EnvFile(
            path=LOAD_TEST_TEMPLATE_ENV_FILE_NAME, prefix="LOAD_TEST_MYAPP"
        )
    ],
    cmd_path=[
        os.path.join(_CURRENT_DIR, "activate-venv.sh"),
        os.path.join(_CURRENT_DIR, "app-load-test.sh"),
    ],
    should_print_cmd_result=False,
)
runner.register(load_test_myapp)
