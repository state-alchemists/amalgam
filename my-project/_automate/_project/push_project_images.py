from zrb.builtin._group import project_group
from zrb import Task, runner
from ..fastapp.image import push_fastapp_image

push_project_images = Task(
    name='push-images',
    group=project_group,
    upstreams=[push_fastapp_image],
    description='Build project images',
    run=lambda *args, **kwargs: kwargs.get('_task').print_out('👌')
)
runner.register(push_project_images)
