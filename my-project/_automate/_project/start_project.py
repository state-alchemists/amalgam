from zrb.builtin._group import project_group
from zrb import Task, runner
from ..fastapp.local import start_fastapp

start_project = Task(
    name='start',
    group=project_group,
    upstreams=[start_fastapp],
    description='Start project',
    run=lambda *args, **kwargs: kwargs.get('_task').print_out('👌')
)
runner.register(start_project)
