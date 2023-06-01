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
compose_env_prefix = 'CONTAINER_MYAPP'

###############################################################################
# Task Definitions
###############################################################################

build_myapp_image = DockerComposeTask(
    icon='🏭',
    name='build-myapp-image',
    description='Build myapp image',
    group=project_group,
    inputs=compose_inputs,
    envs=[image_env],
    skip_execution='{{not input.local_myapp}}',
    cwd=RESOURCE_DIR,
    compose_cmd='build',
    compose_args=[
        'myapp'
    ],
    compose_env_prefix=compose_env_prefix,
)
runner.register(build_myapp_image)

push_myapp_image = DockerComposeTask(
    icon='📰',
    name='push-myapp-image',
    description='Push myapp image',
    group=project_group,
    inputs=compose_inputs,
    envs=[image_env],
    upstreams=[build_myapp_image],
    cwd=RESOURCE_DIR,
    compose_cmd='push',
    compose_args=[
        'myapp'
    ],
    compose_env_prefix=compose_env_prefix,
)
runner.register(push_myapp_image)
