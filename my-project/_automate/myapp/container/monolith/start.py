from zrb import DockerComposeTask, runner

from ...._project import start_project_containers
from ..._checker import (
    app_container_checker,
    kafka_outside_checker,
    kafka_plaintext_checker,
    pandaproxy_outside_checker,
    pandaproxy_plaintext_checker,
    rabbitmq_checker,
    rabbitmq_management_checker,
    redpanda_console_checker,
)
from ..._constant import PREFER_MICROSERVICES, RESOURCE_DIR
from ..._input import host_input, https_input, local_input
from ...image._env import image_env
from ...image._input import image_input
from .._env import compose_env_file, host_port_env
from .._input import enable_monitoring_input
from .._service_config import myapp_service_configs
from ._group import myapp_monolith_container_group
from ._helper import activate_monolith_compose_profile
from .init import init_myapp_monolith_container

start_myapp_monolith_container = DockerComposeTask(
    icon="🐳",
    name="start",
    description="Start myapp container",
    group=myapp_monolith_container_group,
    inputs=[
        local_input,
        enable_monitoring_input,
        host_input,
        https_input,
        image_input,
    ],
    should_execute="{{ input.local_myapp}}",
    upstreams=[init_myapp_monolith_container],
    cwd=RESOURCE_DIR,
    setup_cmd=activate_monolith_compose_profile,
    compose_cmd="logs",
    compose_flags=["-f"],
    compose_env_prefix="CONTAINER_MYAPP",
    compose_service_configs=myapp_service_configs,
    env_files=[compose_env_file],
    envs=[
        image_env,
        host_port_env,
    ],
    checkers=[
        app_container_checker,
        rabbitmq_checker,
        rabbitmq_management_checker,
        kafka_outside_checker,
        kafka_plaintext_checker,
        redpanda_console_checker,
        pandaproxy_outside_checker,
        pandaproxy_plaintext_checker,
    ],
)

if not PREFER_MICROSERVICES:
    start_myapp_monolith_container >> start_project_containers

runner.register(start_myapp_monolith_container)
