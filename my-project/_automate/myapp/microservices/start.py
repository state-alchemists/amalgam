import os

from zrb import Task, python_task, runner
from zrb.helper.accessories.color import colored
from zrb.helper.typing import Any

from ..._project import start_project
from .._constant import PREFER_MICROSERVICES
from .._input import host_input, https_input, local_input
from ..container._input import enable_monitoring_input
from ._group import myapp_microservices_group
from .start_gateway import start_myapp_gateway
from .start_microservices import start_myapp_microservices

_CURRENT_DIR = os.path.dirname(__file__)


@python_task(
    icon="🚤",
    name="start",
    description="Start myapp as a microservices",
    group=myapp_microservices_group,
    inputs=[
        local_input,
        enable_monitoring_input,
        host_input,
        https_input,
    ],
    upstreams=[
        start_myapp_gateway,
        *start_myapp_microservices,
    ],
)
def start_myapp_microservices(*args: Any, **kwargs: Any):
    task: Task = kwargs.get("_task")
    task.print_out(colored("Microservices started", color="yellow"))


if PREFER_MICROSERVICES:
    start_myapp_microservices >> start_project

runner.register(start_myapp_microservices)
