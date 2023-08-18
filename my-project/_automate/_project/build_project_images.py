from zrb.builtin._group import project_group
from zrb import Task, runner
from _automate.myapp.image import build_myapp_image

build_project_images = Task(
    name='build-images',
    group=project_group,
    upstreams=[build_myapp_image],
    description='Build project images',
    run=lambda *args, **kwargs: kwargs.get('_task').print_out('🆗')
)
runner.register(build_project_images)
