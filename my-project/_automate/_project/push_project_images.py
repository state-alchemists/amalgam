from zrb.builtin.group import project_group
from zrb import Task, runner
from _automate.myapp.image import push_myapp_image

push_project_images = Task(
    name='push-images',
    group=project_group,
    upstreams=[push_myapp_image],
    description='Build project images',
    run=lambda *args, **kwargs: kwargs.get('_task').print_out('🆗')
)
runner.register(push_project_images)
