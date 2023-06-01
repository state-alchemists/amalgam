from typing import List
from zrb import Input, DockerComposeTask, runner
from zrb.builtin._group import project_group
from ._common import (
    RESOURCE_DIR,
    local_input, image_input, image_env
)

compose_inputs: List[Input] = [
    local_input,
    image_input,
]
compose_env_prefix = 'CONTAINER_FASTAPP'

###############################################################################
# Task Definitions
###############################################################################

build_fastapp_image = DockerComposeTask(
    icon='🏭',
    name='build-fastapp-image',
    description='Build fastapp image',
    group=project_group,
    inputs=compose_inputs,
    envs=[image_env],
    skip_execution='{{not input.local_fastapp}}',
    cwd=RESOURCE_DIR,
    compose_cmd='build',
    compose_args=[
        'fastapp'
    ],
    compose_env_prefix=compose_env_prefix,
)
runner.register(build_fastapp_image)

push_fastapp_image = DockerComposeTask(
    icon='📰',
    name='push-fastapp-image',
    description='Push fastapp image',
    group=project_group,
    inputs=compose_inputs,
    envs=[image_env],
    upstreams=[build_fastapp_image],
    cwd=RESOURCE_DIR,
    compose_cmd='push',
    compose_args=[
        'fastapp'
    ],
    compose_env_prefix=compose_env_prefix,
)
runner.register(push_fastapp_image)
