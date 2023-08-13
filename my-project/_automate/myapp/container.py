from typing import Mapping, Any, List
from zrb import DockerComposeTask, Env, ServiceConfig, EnvFile, runner, Task
from zrb.helper.util import to_kebab_case
from zrb.builtin._group import project_group
from ._common import (
    APP_TEMPLATE_ENV_FILE_NAME, RESOURCE_DIR, MODULES, app_container_checker,
    rabbitmq_checker, rabbitmq_management_checker, redpanda_console_checker,
    kafka_outside_checker, kafka_plaintext_checker, pandaproxy_outside_checker,
    pandaproxy_plaintext_checker, local_input, run_mode_input,
    enable_monitoring_input, host_input, https_input, app_enable_otel_env
)
from .image import build_myapp_image, image_input, image_env
import os

DOCKER_COMPOSE_APP_ENV_FILE_NAME = os.path.join(
    RESOURCE_DIR, 'docker-compose-app.env'
)

###############################################################################
# Functions
###############################################################################


def setup_runtime_compose_profile(*args: Any, **kwargs: Any) -> str:
    task: Task = kwargs.get('_task')
    env_map = task.get_env_map()
    compose_profiles: List[str] = [
        kwargs.get('myapp_run_mode', 'monolith'),
    ]
    broker_type = env_map.get('APP_BROKER_TYPE', 'rabbitmq')
    if broker_type in ['rabbitmq', 'kafka']:
        compose_profiles.append(broker_type)
    if kwargs.get('enable_myapp_monitoring', False):
        compose_profiles.append('monitoring')
    compose_profile_str = ','.join(compose_profiles)
    return f'export COMPOSE_PROFILES={compose_profile_str}'


def setup_all_compose_profile(*args: Any, **kwargs: Any) -> str:
    compose_profiles = [
        'monitoring',
        'monolith',
        'microservices',
        'kafka',
        'rabbitmq'
    ]
    compose_profile_str = ','.join(compose_profiles)
    return f'export COMPOSE_PROFILES={compose_profile_str}'


def skip_execution(*args: Any, **kwargs: Any) -> bool:
    return not kwargs.get('local_myapp', True)


###############################################################################
# Env File Definitions
###############################################################################

compose_env_file = EnvFile(
    env_file=os.path.join(RESOURCE_DIR, 'docker-compose.env'),
    prefix='CONTAINER_MYAPP'
)

###############################################################################
# Compose Service Config Definitions
###############################################################################

service_configs: Mapping[str, ServiceConfig] = {}
service_names = [to_kebab_case(module) + '-service' for module in MODULES]
for suffix in ['', 'gateway'] + service_names:
    service_suffix = '-' + suffix if suffix != '' else ''
    service_name = f'myapp{service_suffix}'
    service_configs[service_name] = ServiceConfig(
        env_files=[
            EnvFile(
                env_file=APP_TEMPLATE_ENV_FILE_NAME,
                prefix='CONTAINER_MYAPP'
            ),
            EnvFile(
                env_file=DOCKER_COMPOSE_APP_ENV_FILE_NAME,
                prefix='CONTAINER_MYAPP'
            )
        ],
        envs=[
            Env(
                name='APP_OTEL_EXPORTER_OTLP_ENDPOINT',
                os_name='',
                default='http://otel-collector:4317'
            )
        ]
    )

###############################################################################
# Task Definitions
###############################################################################

remove_myapp_container = DockerComposeTask(
    icon='💨',
    name='remove-myapp-container',
    description='Remove myapp container',
    group=project_group,
    cwd=RESOURCE_DIR,
    setup_cmd=setup_all_compose_profile,
    compose_cmd='down',
    compose_env_prefix='CONTAINER_MYAPP',
    compose_service_configs=service_configs,
    envs=[image_env],
    env_files=[compose_env_file]
)
runner.register(remove_myapp_container)

init_myapp_container = DockerComposeTask(
    icon='🔥',
    name='init-myapp-container',
    group=project_group,
    inputs=[
        local_input,
        enable_monitoring_input,
        run_mode_input,
        host_input,
        image_input,
    ],
    skip_execution=skip_execution,
    upstreams=[
        build_myapp_image,
        remove_myapp_container
    ],
    cwd=RESOURCE_DIR,
    setup_cmd=setup_runtime_compose_profile,
    compose_cmd='up',
    compose_flags=['-d'],
    compose_env_prefix='CONTAINER_MYAPP',
    compose_service_configs=service_configs,
    envs=[
        image_env,
        app_enable_otel_env,
    ],
    env_files=[compose_env_file],
)

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
    skip_execution=skip_execution,
    upstreams=[init_myapp_container],
    cwd=RESOURCE_DIR,
    setup_cmd=setup_runtime_compose_profile,
    compose_cmd='logs',
    compose_flags=['-f'],
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
    setup_cmd=setup_all_compose_profile,
    compose_cmd='stop',
    compose_env_prefix='CONTAINER_MYAPP',
    compose_service_configs=service_configs,
    envs=[image_env],
    env_files=[compose_env_file]
)
runner.register(stop_myapp_container)
