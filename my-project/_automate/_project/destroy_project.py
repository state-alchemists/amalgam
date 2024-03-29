from zrb import Task, runner
from zrb.builtin.group import project_group
from _automate.myapp.deployment import destroy_myapp

destroy_project = Task(
    name="destroy",
    group=project_group,
    upstreams=[destroy_myapp],
    description="Remove project deployment",
    run=lambda *args, **kwargs: kwargs.get("_task").print_out("🆗"),
)
runner.register(destroy_project)
