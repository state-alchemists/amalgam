from zrb import Task, runner
from zrb.builtin.group import project_group
from _automate.myapp.container import stop_myapp_container

stop_project_containers = Task(
    name="stop-containers",
    group=project_group,
    upstreams=[stop_myapp_container],
    description="Stop project containers",
    run=lambda *args, **kwargs: kwargs.get("_task").print_out("🆗"),
)
runner.register(stop_project_containers)
