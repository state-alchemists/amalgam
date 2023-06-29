from zrb import CmdTask, DockerComposeTask, Task, Env, EnvFile, runner
from zrb.builtin._group import project_group
from ._common import (
    CURRENT_DIR, APP_DIR, APP_TEMPLATE_ENV_FILE_NAME, RESOURCE_DIR,
    SKIP_SUPPORT_CONTAINER_EXECUTION, SKIP_LOCAL_MONOLITH_EXECUTION,
    SKIP_LOCAL_MICROSERVICES_EXECUTION,
    rabbitmq_checker, rabbitmq_management_checker,
    redpanda_console_checker, kafka_outside_checker,
    kafka_plaintext_checker, pandaproxy_outside_checker,
    pandaproxy_plaintext_checker, app_local_checker,
    local_input, run_mode_input, host_input, https_input,
    local_app_port_env, local_app_broker_type_env
)
from .image import build_myapp_image, image_input
from .frontend import build_myapp_frontend
from .container import remove_myapp_container
from .local_microservices import get_start_microservices
import os

start_broker_compose_profile = '{{env.get("APP_BROKER_TYPE", "rabbitmq")}}'


###############################################################################
# Env file Definitions
###############################################################################

app_env_file = EnvFile(
    env_file=APP_TEMPLATE_ENV_FILE_NAME, prefix='MYAPP'
)

###############################################################################
# Task Definitions
###############################################################################

init_myapp_support_container = DockerComposeTask(
    icon='🔥',
    name='init-myapp-support-container',
    inputs=[
        local_input,
        host_input,
        image_input,
    ],
    skip_execution=SKIP_SUPPORT_CONTAINER_EXECUTION,
    upstreams=[
        remove_myapp_container
    ],
    cwd=RESOURCE_DIR,
    setup_cmd=f'export COMPOSE_PROFILES={start_broker_compose_profile}',
    compose_cmd='up',
    compose_flags=['-d'],
    compose_env_prefix='CONTAINER_MYAPP',
    envs=[
        local_app_broker_type_env,
        local_app_port_env,
    ],
)

start_myapp_support_container = DockerComposeTask(
    icon='🐳',
    name='start-myapp-support-container',
    description='Start myapp container',
    inputs=[
        local_input,
        host_input,
        https_input,
        image_input,
    ],
    skip_execution=SKIP_SUPPORT_CONTAINER_EXECUTION,
    upstreams=[init_myapp_support_container],
    cwd=RESOURCE_DIR,
    setup_cmd=f'export COMPOSE_PROFILES={start_broker_compose_profile}',
    compose_cmd='logs',
    compose_flags=['-f'],
    compose_env_prefix='CONTAINER_MYAPP',
    envs=[
        local_app_broker_type_env,
        local_app_port_env,
    ],
    checkers=[
        rabbitmq_checker,
        rabbitmq_management_checker,
        kafka_outside_checker,
        kafka_plaintext_checker,
        redpanda_console_checker,
        pandaproxy_outside_checker,
        pandaproxy_plaintext_checker,
    ]
)

prepare_myapp_backend = CmdTask(
    icon='🚤',
    name='prepare-myapp-backend',
    description='Prepare backend for myapp',
    group=project_group,
    cwd=APP_DIR,
    cmd_path=os.path.join(CURRENT_DIR, 'cmd', 'prepare-backend.sh'),
)
runner.register(prepare_myapp_backend)

start_monolith_myapp = CmdTask(
    icon='🚤',
    name='start-monolith-myapp',
    inputs=[
        local_input,
        run_mode_input,
        host_input,
        https_input
    ],
    skip_execution=SKIP_LOCAL_MONOLITH_EXECUTION,
    upstreams=[
        start_myapp_support_container,
        build_myapp_frontend,
        prepare_myapp_backend,
    ],
    cwd=APP_DIR,
    env_files=[app_env_file],
    envs=[
        local_app_broker_type_env,
        local_app_port_env,
    ],
    cmd_path=os.path.join(CURRENT_DIR, 'cmd', 'start.sh'),
    checkers=[
        app_local_checker,
    ]
)

start_myapp_gateway = CmdTask(
    icon='🚪',
    name='start-myapp-gateway',
    inputs=[
        local_input,
        run_mode_input,
        host_input,
        https_input
    ],
    skip_execution=SKIP_LOCAL_MICROSERVICES_EXECUTION,
    upstreams=[
        start_myapp_support_container,
        build_myapp_frontend,
        prepare_myapp_backend,
    ],
    cwd=APP_DIR,
    env_files=[app_env_file],
    envs=[
        local_app_broker_type_env,
        local_app_port_env,
        Env(name='APP_DB_AUTO_MIGRATE', default='false', os_name=''),
        Env(name='APP_ENABLE_MESSAGE_CONSUMER', default='false', os_name=''),
        Env(name='APP_ENABLE_RPC_SERVER', default='false', os_name=''),
    ],
    cmd_path=os.path.join(CURRENT_DIR, 'cmd', 'start.sh'),
    checkers=[
        app_local_checker,
    ]
)
runner.register(start_myapp_gateway)

start_microservices = get_start_microservices(
    upstreams=[
        start_myapp_support_container,
        build_myapp_frontend,
        prepare_myapp_backend,
    ]
)

start_myapp = Task(
    icon='🚤',
    name='start-myapp',
    description='Start myapp',
    group=project_group,
    upstreams=[
        start_monolith_myapp,
        start_myapp_gateway,
    ] + start_microservices,
    run=lambda *args, **kwargs: kwargs.get('_task').print_out('🆗')
)
runner.register(start_myapp)
