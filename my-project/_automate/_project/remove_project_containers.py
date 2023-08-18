from zrb.builtin._group import project_group
from zrb import Task, runner
from _automate.myapp.container import remove_myapp_container

remove_project_containers = Task(
    name='remove-containers',
    group=project_group,
    upstreams=[remove_myapp_container],
    description='Remove project containers',
    run=lambda *args, **kwargs: kwargs.get('_task').print_out('🆗')
)
runner.register(remove_project_containers)
