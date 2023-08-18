from zrb.builtin._group import project_group
from zrb import Task, runner
from _automate.myapp.container import start_myapp_container

start_project_containers = Task(
    name='start-containers',
    group=project_group,
    upstreams=[start_myapp_container],
    description='Start as containers',
    run=lambda *args, **kwargs: kwargs.get('_task').print_out('🆗')
)
runner.register(start_project_containers)
