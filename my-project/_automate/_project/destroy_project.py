from zrb.builtin._group import project_group
from zrb import Task, runner
from ..fastapp.deployment import destroy_fastapp

destroy_project = Task(
    name='destroy',
    group=project_group,
    upstreams=[destroy_fastapp],
    description='Remove project deployment',
    run=lambda *args, **kwargs: kwargs.get('_task').print_out('👌')
)
runner.register(destroy_project)
