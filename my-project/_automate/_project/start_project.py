from zrb import Task, runner
from zrb.builtin.group import project_group
from _automate.myapp.local import start_myapp

start_project = Task(
    name="start",
    group=project_group,
    upstreams=[start_myapp],
    description="Start project",
    run=lambda *args, **kwargs: kwargs.get("_task").print_out("🆗"),
)
runner.register(start_project)
