from typing import Mapping
from zrb import DockerComposeTask, ServiceConfig, EnvFile, runner
from zrb.helper.util import to_kebab_case
from zrb.builtin._group import project_group
from ._common import (
    APP_TEMPLATE_ENV_FILE_NAME, CURRENT_DIR, RESOURCE_DIR,
    SKIP_CONTAINER_EXECUTION, MODULES,
    app_container_checker, rabbitmq_checker, rabbitmq_management_checker,
    redpanda_console_checker, kafka_outside_checker, kafka_plaintext_checker,
    pandaproxy_outside_checker, pandaproxy_plaintext_checker, local_input,
    run_mode_input, host_input, https_input
)
from .image import build_myapp_image, image_input, image_env
import os

all_compose_profiles = 'monolith,microservices,kafka,rabbitmq'
start_broker_compose_profile = '{{env.get("APP_BROKER_TYPE", "rabbitmq")}}'
start_mode_compose_profile = '{{input.get("myapp_run_mode", "monolith")}}' # noqa
start_compose_profiles = ','.join([
    start_broker_compose_profile, start_mode_compose_profile
])

###############################################################################
# Env File Definitions
###############################################################################

compose_env_file = EnvFile(
    env_file=os.path.join(CURRENT_DIR, 'config', 'docker-compose.env'),
    prefix='CONTAINER_MYAPP'
)

###############################################################################
# Compose Service Config Definitions
###############################################################################

service_config_env_file = EnvFile(
    env_file=APP_TEMPLATE_ENV_FILE_NAME, prefix='CONTAINER_MYAPP'
)
service_configs: Mapping[str, ServiceConfig] = {
    'myapp': ServiceConfig(env_files=[service_config_env_file])
}
modules = ['gateway'] + MODULES
for module in modules:
    service_name = 'myapp-' + to_kebab_case(module)
    service_configs[service_name] = ServiceConfig(
        env_files=[service_config_env_file]
    )

###############################################################################
# Task Definitions
###############################################################################

remove_myapp_container = DockerComposeTask(
    icon='💨',
    name='remove-myapp-container',
    description='Rumove myapp container',
    group=project_group,
    cwd=RESOURCE_DIR,
    setup_cmd=f'export COMPOSE_PROFILES={all_compose_profiles}',
    compose_cmd='down',
    compose_env_prefix='CONTAINER_MYAPP',
    compose_service_configs=service_configs,
    envs=[image_env],
    env_files=[compose_env_file]
)
runner.register(remove_myapp_container)

start_myapp_container = DockerComposeTask(
    icon='🐳',
    name='start-myapp-container',
    description='Start myapp container',
    group=project_group,
    inputs=[
        local_input,
        run_mode_input,
        host_input,
        https_input,
        image_input,
    ],
    skip_execution=SKIP_CONTAINER_EXECUTION,
    upstreams=[
        build_myapp_image,
        remove_myapp_container
    ],
    cwd=RESOURCE_DIR,
    setup_cmd=f'export COMPOSE_PROFILES={start_compose_profiles}',
    compose_cmd='up',
    compose_env_prefix='CONTAINER_MYAPP',
    compose_service_configs=service_configs,
    envs=[image_env],
    env_files=[compose_env_file],
    checkers=[
        app_container_checker,
        rabbitmq_checker,
        rabbitmq_management_checker,
        kafka_outside_checker,
        kafka_plaintext_checker,
        redpanda_console_checker,
        pandaproxy_outside_checker,
        pandaproxy_plaintext_checker,
    ]
)
runner.register(start_myapp_container)

stop_myapp_container = DockerComposeTask(
    icon='⛔',
    name='stop-myapp-container',
    description='Stop myapp container',
    group=project_group,
    cwd=RESOURCE_DIR,
    setup_cmd=f'export COMPOSE_PROFILES={all_compose_profiles}',
    compose_cmd='stop',
    compose_env_prefix='CONTAINER_MYAPP',
    compose_service_configs=service_configs,
    envs=[image_env],
    env_files=[compose_env_file]
)
runner.register(stop_myapp_container)
