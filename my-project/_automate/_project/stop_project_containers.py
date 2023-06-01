from zrb.builtin._group import project_group
from zrb import Task, runner
from ..fastapp.container import stop_fastapp_container

stop_project_containers = Task(
    name='stop-containers',
    group=project_group,
    upstreams=[stop_fastapp_container],
    description='Stop project containers',
    run=lambda *args, **kwargs: kwargs.get('_task').print_out('👌')
)
runner.register(stop_project_containers)
