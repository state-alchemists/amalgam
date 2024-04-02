import os

from zrb import CmdTask, Env, runner

from ..._project import deploy_project
from .._constant import AUTOMATE_DIR, DEPLOYMENT_DIR, PREFER_MICROSERVICES
from .._env import (
    deployment_app_env_file,
    deployment_config_env_file,
    deployment_enable_monitoring_env,
    deployment_modules_env,
    pulumi_backend_url_env,
    pulumi_config_passphrase_env,
)
from .._input import pulumi_stack_input, replica_input
from ..container._input import enable_monitoring_input
from ..image import push_myapp_image
from ..image._env import image_env
from ..image._input import image_input
from ._group import myapp_microservices_group

_CURRENT_DIR = os.path.dirname(__file__)

deploy_myapp_microservices = CmdTask(
    icon="🚧",
    name="deploy",
    description="Deploy myapp as a microservices",
    group=myapp_microservices_group,
    inputs=[
        image_input,
        replica_input,
        pulumi_stack_input,
        enable_monitoring_input,
    ],
    upstreams=[push_myapp_image],
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
        deployment_enable_monitoring_env,
        Env(
            name="MODE",
            os_name="DEPLOYMENT_CONFIG_MYAPP_MODE",
            default="microservices",
        ),
    ],
    cmd_path=[
        os.path.join(AUTOMATE_DIR, "init-pulumi-stack.sh"),
        os.path.join(_CURRENT_DIR, "deploy.sh"),
    ],
)

if PREFER_MICROSERVICES:
    deploy_myapp_microservices >> deploy_project

runner.register(deploy_myapp_microservices)
