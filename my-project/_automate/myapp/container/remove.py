from zrb import DockerComposeTask, runner

from ..._project import remove_project_containers
from .._constant import RESOURCE_DIR
from ..image._env import image_env
from ._env import compose_env_file
from ._group import myapp_container_group
from ._helper import activate_all_compose_profile
from ._service_config import myapp_service_configs

remove_myapp_container = DockerComposeTask(
    icon="💨",
    name="remove",
    description="Remove myapp container",
    group=myapp_container_group,
    cwd=RESOURCE_DIR,
    setup_cmd=activate_all_compose_profile,
    compose_cmd="down",
    compose_env_prefix="CONTAINER_MYAPP",
    compose_service_configs=myapp_service_configs,
    env_files=[compose_env_file],
    envs=[image_env],
)

remove_myapp_container >> remove_project_containers

runner.register(remove_myapp_container)
