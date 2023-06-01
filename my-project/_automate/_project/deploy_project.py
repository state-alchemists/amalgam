from zrb.builtin._group import project_group
from zrb import Task, runner
from ..myapp.deployment import deploy_myapp

deploy_project = Task(
    name='deploy',
    group=project_group,
    upstreams=[deploy_myapp],
    description='Deploy project',
    run=lambda *args, **kwargs: kwargs.get('_task').print_out('👌')
)
runner.register(deploy_project)
