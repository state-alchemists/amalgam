import os
from typing import List

from zrb import CmdTask, HTTPChecker, Task
from zrb.helper.util import to_kebab_case

from .._constant import APP_DIR, AUTOMATE_DIR, MODULES
from .._input import host_input, https_input, local_input
from ..backend import prepare_myapp_backend
from ..container._input import enable_monitoring_input
from ..container.support import start_myapp_support_container
from ..frontend import build_myapp_frontend
from ._helper import get_disable_all_module_envs, get_service_env_file, get_service_envs

_CURRENT_DIR = os.path.dirname(__file__)


_disable_all_module_envs = get_disable_all_module_envs()
start_myapp_microservices: List[Task] = []
for _module_index, _module_name in enumerate(MODULES):
    _service_env_file = get_service_env_file(_module_name)
    _service_envs = get_service_envs(3000, _module_index, _module_name)
    _kebab_module_name = to_kebab_case(_module_name)
    # Define start service task
    _start_service = CmdTask(
        name=f"start-{_kebab_module_name}-service",
        inputs=[
            local_input,
            host_input,
            https_input,
            enable_monitoring_input,
        ],
        upstreams=[
            start_myapp_support_container,
            build_myapp_frontend,
            prepare_myapp_backend,
        ],
        cwd=APP_DIR,
        env_files=[_service_env_file],
        envs=[*_disable_all_module_envs, *_service_envs],
        cmd_path=[
            os.path.join(AUTOMATE_DIR, "activate-venv.sh"),
            os.path.join(_CURRENT_DIR, "start.sh"),
        ],
        checkers=[
            HTTPChecker(
                name=f"check-myapp-{_kebab_module_name}-service",
                host="{{input.myapp_host}}",
                url="/readiness",
                port="{{env.APP_PORT}}",
                is_https="{{input.myapp_https}}",
            )
        ],
    )
    start_myapp_microservices.append(_start_service)
