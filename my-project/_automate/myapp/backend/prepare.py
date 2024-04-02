import os

from zrb import CmdTask, runner

from .._constant import APP_DIR, AUTOMATE_DIR
from ._group import myapp_backend_group

_CURRENT_DIR = os.path.dirname(__file__)

prepare_myapp_backend = CmdTask(
    icon="🚤",
    name="prepare",
    description="Prepare backend for myapp",
    group=myapp_backend_group,
    cwd=APP_DIR,
    cmd_path=[
        os.path.join(AUTOMATE_DIR, "activate-venv.sh"),
        os.path.join(_CURRENT_DIR, "prepare.sh"),
    ],
)
runner.register(prepare_myapp_backend)
