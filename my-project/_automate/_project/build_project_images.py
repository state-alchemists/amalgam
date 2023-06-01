from zrb.builtin._group import project_group
from zrb import Task, runner
from ..fastapp.image import build_fastapp_image

build_project_images = Task(
    name='build-images',
    group=project_group,
    upstreams=[build_fastapp_image],
    description='Build project images',
    run=lambda *args, **kwargs: kwargs.get('_task').print_out('👌')
)
runner.register(build_project_images)
