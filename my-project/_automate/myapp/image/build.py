from zrb import BoolInput, DockerComposeTask, runner

from ..._project import build_project, build_project_images
from .._constant import RESOURCE_DIR
from .._input import local_input
from ._env import image_env
from ._group import myapp_image_group
from ._input import image_input

build_myapp_image = DockerComposeTask(
    icon="🏭",
    name="build",
    description="Build myapp image",
    group=myapp_image_group,
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

build_myapp_image >> build_project_images
build_myapp_image >> build_project

runner.register(build_myapp_image)
