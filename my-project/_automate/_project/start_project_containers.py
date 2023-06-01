from zrb.builtin._group import project_group
from zrb import Task, runner
from ..fastapp.container import start_fastapp_container

start_project_containers = Task(
    name='start-containers',
    group=project_group,
    upstreams=[start_fastapp_container],
    description='Start as containers',
    run=lambda *args, **kwargs: kwargs.get('_task').print_out('👌')
)
runner.register(start_project_containers)
