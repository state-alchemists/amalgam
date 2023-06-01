from typing import List
from zrb import CmdTask, Env, EnvFile, runner
from zrb.builtin._group import project_group
from .image import push_fastapp_image
from ._common import (
    CURRENT_DIR, DEPLOYMENT_DIR, APP_TEMPLATE_ENV_FILE_NAME,
    DEPLOYMENT_TEMPLATE_ENV_FILE_NAME, MODULES, image_input,
    pulumi_stack_input, mode_input, image_env, pulumi_backend_url_env,
    pulumi_config_passphrase_env
)
import os
import jsons

deployment_app_env_file = EnvFile(
    env_file=APP_TEMPLATE_ENV_FILE_NAME,
    prefix='DEPLOYMENT_APP_FASTAPP'
)
deployment_env_file = EnvFile(
    env_file=DEPLOYMENT_TEMPLATE_ENV_FILE_NAME,
    prefix='DEPLOYMENT_CONFIG_FASTAPP'
)

deployment_modules_env = Env(
    name='MODULES',
    os_name='DEPLOYMENT_CONFIG_FASTAPP_MODULES',
    default=jsons.dumps(MODULES)
)

deployment_envs: List[Env] = [
    pulumi_backend_url_env,
    pulumi_config_passphrase_env,
    image_env,
    deployment_modules_env
]

deployment_mode_env = Env(
    name='MODE',
    os_name='DEPLOYMENT_CONFIG_FASTAPP_MODE',
    default='{{input.fastapp_mode}}'
)


###############################################################################
# Task Definitions
###############################################################################

deploy_fastapp = CmdTask(
    icon='🚧',
    name='deploy-fastapp',
    description='Deploy fastapp',
    group=project_group,
    inputs=[
        image_input,
        pulumi_stack_input,
        mode_input,
    ],
    upstreams=[push_fastapp_image],
    cwd=DEPLOYMENT_DIR,
    env_files=[
        deployment_env_file,
        deployment_app_env_file,
    ],
    envs=deployment_envs + [
        deployment_mode_env,
    ],
    cmd_path=os.path.join(CURRENT_DIR, 'cmd', 'pulumi-up.sh'),
)
runner.register(deploy_fastapp)

destroy_fastapp = CmdTask(
    icon='💨',
    name='destroy-fastapp',
    description='Remove fastapp deployment',
    group=project_group,
    inputs=[
        pulumi_stack_input,
    ],
    cwd=DEPLOYMENT_DIR,
    env_files=[
        deployment_env_file,
        deployment_app_env_file,
    ],
    envs=deployment_envs,
    cmd_path=os.path.join(CURRENT_DIR, 'cmd', 'pulumi-destroy.sh'),
)
runner.register(destroy_fastapp)
