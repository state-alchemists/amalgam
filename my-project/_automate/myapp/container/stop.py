from zrb import DockerComposeTask, runner

from ..._project import stop_project_containers
from .._constant import RESOURCE_DIR
from ..image._env import image_env
from ._env import compose_env_file, host_port_env
from ._group import myapp_container_group
from ._service_config import myapp_service_configs

###############################################################################
# ⚙️ kebab-zrb-task-name
###############################################################################

stop_myapp_container = DockerComposeTask(
    icon="⛔",
    name="stop",
    description="Stop myapp container",
    group=myapp_container_group,
    cwd=RESOURCE_DIR,
    compose_cmd="stop",
    compose_env_prefix="CONTAINER_MYAPP",
    compose_service_configs=myapp_service_configs,
    env_files=[compose_env_file],
    envs=[
        image_env,
        host_port_env,
    ],
)

stop_myapp_container >> stop_project_containers

runner.register(stop_myapp_container)
