from zrb import BoolInput, DockerComposeTask, runner
from zrb.builtin.group import project_group

from ._config import RESOURCE_DIR
from ._env import image_env
from ._input import image_input, local_input

###############################################################################
# ⚙️ build-kebab-zrb-task-name-image
###############################################################################

build_myapp_image = DockerComposeTask(
    icon="🏭",
    name="build-myapp-image",
    description="Build myapp image",
    group=project_group,
    inputs=[
        local_input,
        image_input,
        BoolInput(
            name="build-myapp-with-cache",
            prompt="Build myapp image with Cache",
            default=True,
        ),
    ],
    envs=[image_env],
    should_execute="{{ input.local_myapp}}",
    cwd=RESOURCE_DIR,
    compose_cmd="build",
    compose_args=["myapp"],
    compose_flags=[
        "{{ '--no-cache' if not input.build_myapp_with_cache else '' }}"
    ],
    compose_env_prefix="CONTAINER_MYAPP",
)
runner.register(build_myapp_image)

###############################################################################
# ⚙️ push-kebab-zrb-task-name-image
###############################################################################

push_myapp_image = DockerComposeTask(
    icon="📰",
    name="push-myapp-image",
    description="Push myapp image",
    group=project_group,
    inputs=[
        local_input,
        image_input,
    ],
    envs=[image_env],
    upstreams=[build_myapp_image],
    cwd=RESOURCE_DIR,
    compose_cmd="push",
    compose_args=["myapp"],
    compose_env_prefix="CONTAINER_MYAPP",
)
runner.register(push_myapp_image)
