from zrb import DockerComposeTask, Env, StrInput, runner
from zrb.builtin.group import project_group
from ._common import RESOURCE_DIR, local_input

###############################################################################
# Input Definitions
###############################################################################

image_input = StrInput(
    name='myapp-image',
    description='Image name of "myapp"',
    prompt='Image name of "myapp"',
    default='docker.io/gofrendi/myapp:latest'
)

###############################################################################
# Env fDefinitions
###############################################################################

image_env = Env(
    name='IMAGE',
    os_name='CONTAINER_MYAPP_IMAGE',
    default='{{input.myapp_image}}'
)

###############################################################################
# Task Definitions
###############################################################################

build_myapp_image = DockerComposeTask(
    icon='🏭',
    name='build-myapp-image',
    description='Build myapp image',
    group=project_group,
    inputs=[
        local_input,
        image_input,
    ],
    envs=[image_env],
    skip_execution='{{not input.local_myapp}}',
    cwd=RESOURCE_DIR,
    compose_cmd='build',
    compose_args=[
        'myapp'
    ],
    compose_env_prefix='CONTAINER_MYAPP',
)
runner.register(build_myapp_image)

push_myapp_image = DockerComposeTask(
    icon='📰',
    name='push-myapp-image',
    description='Push myapp image',
    group=project_group,
    inputs=[
        local_input,
        image_input,
    ],
    envs=[image_env],
    upstreams=[build_myapp_image],
    cwd=RESOURCE_DIR,
    compose_cmd='push',
    compose_args=[
        'myapp'
    ],
    compose_env_prefix='CONTAINER_MYAPP',
)
runner.register(push_myapp_image)
