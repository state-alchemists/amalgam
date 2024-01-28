import os

from zrb import EnvFile

from ._config import (
    APP_TEMPLATE_ENV_FILE_NAME,
    DEPLOYMENT_TEMPLATE_ENV_FILE_NAME,
    RESOURCE_DIR,
)

app_env_file = EnvFile(path=APP_TEMPLATE_ENV_FILE_NAME, prefix="MYAPP")

compose_env_file = EnvFile(
    path=os.path.join(RESOURCE_DIR, "docker-compose.env"),
    prefix="CONTAINER_MYAPP",
)

deployment_app_env_file = EnvFile(
    path=APP_TEMPLATE_ENV_FILE_NAME, prefix="DEPLOYMENT_APP_MYAPP"
)

deployment_config_env_file = EnvFile(
    path=DEPLOYMENT_TEMPLATE_ENV_FILE_NAME, prefix="DEPLOYMENT_CONFIG_MYAPP"
)
