from zrb import CmdTask, Env, EnvFile, PathChecker, runner
from zrb.builtin._group import project_group
from ._common import (
    APP_FRONTEND_DIR, APP_FRONTEND_BUILD_DIR, CURRENT_DIR,
    APP_TEMPLATE_ENV_FILE_NAME, local_app_port_env
)
import os

###############################################################################
# Task Definitions
###############################################################################

build_fastapp_frontend = CmdTask(
    icon='🚤',
    name='build-fastapp-frontend',
    description='Build frontend for fastapp',
    group=project_group,
    cwd=APP_FRONTEND_DIR,
    cmd_path=os.path.join(CURRENT_DIR, 'cmd', 'build-frontend.sh'),
    checkers=[
        PathChecker(
            name='check-fastapp-frontend-build',
            path=APP_FRONTEND_BUILD_DIR
        )
    ],
    env_files=[
        EnvFile(
            env_file=APP_TEMPLATE_ENV_FILE_NAME, prefix='FASTAPP'
        ),
    ],
    envs=[
        local_app_port_env,
        Env(name='WATCH', os_name='', default='1')
    ]
)
runner.register(build_fastapp_frontend)

build_fastapp_frontend_once = CmdTask(
    icon='🚤',
    name='build-fastapp-frontend_once',
    description='Build frontend for fastapp',
    group=project_group,
    cwd=APP_FRONTEND_DIR,
    cmd_path=os.path.join(CURRENT_DIR, 'cmd', 'build-frontend.sh'),
    checkers=[
        PathChecker(
            name='check-fastapp-frontend-build',
            path=APP_FRONTEND_BUILD_DIR
        )
    ],
    env_files=[
        EnvFile(
            env_file=APP_TEMPLATE_ENV_FILE_NAME, prefix='FASTAPP'
        ),
    ],
    envs=[
        local_app_port_env,
        Env(name='WATCH', os_name='', default='0')
    ]
)
