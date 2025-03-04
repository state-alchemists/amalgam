import os

from zrb import CmdTask

from myapp._zrb.config import ACTIVATE_VENV_SCRIPT, APP_DIR

create_venv = CmdTask(
    name="create-myapp-venv",
    cwd=APP_DIR,
    cmd="python -m venv .venv",
    execute_condition=lambda _: not os.path.isdir(os.path.join(APP_DIR, ".venv")),
)

prepare_venv = CmdTask(
    name="prepare-myapp-venv",
    cmd=[ACTIVATE_VENV_SCRIPT, "pip install -r requirements.txt"],
    cwd=APP_DIR,
)
create_venv >> prepare_venv
