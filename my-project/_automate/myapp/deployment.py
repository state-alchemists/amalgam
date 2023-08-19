from zrb import CmdTask, Env, EnvFile, StrInput, ChoiceInput, runner
from zrb.builtin.group import project_group
from .image import push_myapp_image
from ._common import (
    CURRENT_DIR, DEPLOYMENT_DIR, APP_TEMPLATE_ENV_FILE_NAME,
    DEPLOYMENT_TEMPLATE_ENV_FILE_NAME, MODULES,
    enable_monitoring_input
)
from .image import image_input, image_env
import os
import jsons


###############################################################################
# Input Definitions
###############################################################################

deploy_mode_input = ChoiceInput(
    name='myapp-deploy-mode',
    description='"myapp" deploy mode (monolith/microservices)',
    prompt='Deploy "myapp" as a monolith or microservices?',
    choices=['monolith', 'microservices'],
    default='monolith'
)

pulumi_stack_input = StrInput(
    name='myapp-pulumi-stack',
    description='Pulumi stack name for "myapp"',
    prompt='Pulumi stack name for "myapp"',
    default=os.getenv('ZRB_ENV', 'dev')
)

###############################################################################
# Env Definitions
###############################################################################

pulumi_backend_url_env = Env(
    name='PULUMI_BACKEND_URL',
    os_name='PULUMI_MYAPP_BACKEND_URL',
    default=f'file://{DEPLOYMENT_DIR}/state'
)

pulumi_config_passphrase_env = Env(
    name='PULUMI_CONFIG_PASSPHRASE',
    os_name='PULUMI_MYAPP_CONFIG_PASSPHRASE',
    default='secret'
)

###############################################################################
# Env File Definitions
###############################################################################

deployment_app_env_file = EnvFile(
    env_file=APP_TEMPLATE_ENV_FILE_NAME,
    prefix='DEPLOYMENT_APP_MYAPP'
)
deployment_env_file = EnvFile(
    env_file=DEPLOYMENT_TEMPLATE_ENV_FILE_NAME,
    prefix='DEPLOYMENT_CONFIG_MYAPP'
)

deployment_modules_env = Env(
    name='MODULES',
    os_name='DEPLOYMENT_CONFIG_MYAPP_MODULES',
    default=jsons.dumps(MODULES)
)

deployment_mode_env = Env(
    name='MODE',
    os_name='DEPLOYMENT_CONFIG_MYAPP_MODE',
    default='{{input.myapp_deploy_mode}}'
)

deployment_enable_monitoring_env = Env(
    name='ENABLE_MONITORING',
    os_name='DEPLOYMENT_CONFIG_MYAPP_ENABLE_MONITORING',
    default='{{ 1 if input.enable_myapp_monitoring else 0 }}'
)

###############################################################################
# Task Definitions
###############################################################################

deploy_myapp = CmdTask(
    icon='🚧',
    name='deploy-myapp',
    description='Deploy myapp',
    group=project_group,
    inputs=[
        image_input,
        pulumi_stack_input,
        deploy_mode_input,
        enable_monitoring_input,
    ],
    upstreams=[push_myapp_image],
    cwd=DEPLOYMENT_DIR,
    env_files=[
        deployment_env_file,
        deployment_app_env_file,
    ],
    envs=[
        pulumi_backend_url_env,
        pulumi_config_passphrase_env,
        image_env,
        deployment_modules_env,
        deployment_mode_env,
        deployment_enable_monitoring_env,
    ],
    cmd_path=[
        os.path.join(CURRENT_DIR, 'cmd', 'pulumi-init-stack.sh'),
        os.path.join(CURRENT_DIR, 'cmd', 'pulumi-destroy.sh'),
    ]
)
runner.register(deploy_myapp)

destroy_myapp = CmdTask(
    icon='💨',
    name='destroy-myapp',
    description='Remove myapp deployment',
    group=project_group,
    inputs=[
        pulumi_stack_input,
    ],
    cwd=DEPLOYMENT_DIR,
    env_files=[
        deployment_env_file,
        deployment_app_env_file,
    ],
    envs=[
        pulumi_backend_url_env,
        pulumi_config_passphrase_env,
        image_env,
        deployment_modules_env,
    ],
    cmd_path=[
        os.path.join(CURRENT_DIR, 'cmd', 'pulumi-init-stack.sh'),
        os.path.join(CURRENT_DIR, 'cmd', 'pulumi-destroy.sh'),
    ]
)
runner.register(destroy_myapp)
