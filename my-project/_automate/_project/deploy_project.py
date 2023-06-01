from zrb.builtin._group import project_group
from zrb import Task, runner
from ..fastapp.deployment import deploy_fastapp

deploy_project = Task(
    name='deploy',
    group=project_group,
    upstreams=[deploy_fastapp],
    description='Deploy project',
    run=lambda *args, **kwargs: kwargs.get('_task').print_out('👌')
)
runner.register(deploy_project)
