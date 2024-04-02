import os

from zrb import CmdTask, Env

from .._checker import app_local_checker
from .._constant import APP_DIR, AUTOMATE_DIR
from .._env import app_enable_otel_env, app_env_file
from .._input import host_input, https_input, local_input
from ..backend import prepare_myapp_backend
from ..container._input import enable_monitoring_input
from ..container.support import start_myapp_support_container
from ..frontend import build_myapp_frontend

_CURRENT_DIR = os.path.dirname(__file__)

start_myapp_gateway = CmdTask(
    icon="🚪",
    name="start-myapp-gateway",
    inputs=[
        local_input,
        enable_monitoring_input,
        host_input,
        https_input,
    ],
    upstreams=[
        start_myapp_support_container,
        build_myapp_frontend,
        prepare_myapp_backend,
    ],
    cwd=APP_DIR,
    env_files=[
        app_env_file,
    ],
    envs=[
        Env(name="APP_DB_AUTO_MIGRATE", default="false", os_name=""),
        Env(name="APP_ENABLE_EVENT_HANDLER", default="false", os_name=""),
        Env(name="APP_ENABLE_RPC_SERVER", default="false", os_name=""),
        app_enable_otel_env,
    ],
    cmd_path=[
        os.path.join(AUTOMATE_DIR, "activate-venv.sh"),
        os.path.join(_CURRENT_DIR, "start.sh"),
    ],
    checkers=[
        app_local_checker,
    ],
)
