import os

from zrb import CmdTask, runner

from .._project import destroy_project
from ._constant import DEPLOYMENT_DIR
from ._env import (
    deployment_app_env_file,
    deployment_config_env_file,
    deployment_modules_env,
    pulumi_backend_url_env,
    pulumi_config_passphrase_env,
)
from ._group import myapp_group
from ._input import pulumi_stack_input
from .image._env import image_env

_CURRENT_DIR = os.path.dirname(__file__)

destroy_myapp = CmdTask(
    icon="💨",
    name="destroy",
    description="Destroy myapp deployment",
    group=myapp_group,
    inputs=[
        pulumi_stack_input,
    ],
    cwd=DEPLOYMENT_DIR,
    env_files=[
        deployment_config_env_file,
        deployment_app_env_file,
    ],
    envs=[
        pulumi_backend_url_env,
        pulumi_config_passphrase_env,
        image_env,
        deployment_modules_env,
    ],
    cmd_path=[
        os.path.join(_CURRENT_DIR, "init-pulumi-stack.sh"),
        os.path.join(_CURRENT_DIR, "destroy.sh"),
    ],
)

destroy_myapp >> destroy_project

runner.register(destroy_myapp)
