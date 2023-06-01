from zrb.builtin._group import project_group
from zrb import Task, runner
from ..fastapp.container import remove_fastapp_container

remove_project_containers = Task(
    name='remove-containers',
    group=project_group,
    upstreams=[remove_fastapp_container],
    description='Remove project containers',
    run=lambda *args, **kwargs: kwargs.get('_task').print_out('👌')
)
runner.register(remove_project_containers)
