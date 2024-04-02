from zrb import DockerComposeTask, runner

from ..._project import publish_project, push_project_images
from .._constant import RESOURCE_DIR
from .._input import local_input
from ._env import image_env
from ._group import myapp_image_group
from ._input import image_input
from .build import build_myapp_image

push_myapp_image = DockerComposeTask(
    icon="📰",
    name="push",
    description="Push myapp image",
    group=myapp_image_group,
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

push_myapp_image >> push_project_images
push_myapp_image >> publish_project

runner.register(push_myapp_image)
