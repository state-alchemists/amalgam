from zrb.task.cmd_task import CmdTask

from myapp._zrb.config import APP_DIR
from myapp._zrb.group import app_group

format_myapp_code = app_group.add_task(
    CmdTask(
        name="format-myapp-code",
        description="✨ Format Python code",
        cmd=[
            "isort . --profile black --force-grid-wrap 0",
            "black .",
        ],
        cwd=APP_DIR,
    ),
    alias="format",
)
