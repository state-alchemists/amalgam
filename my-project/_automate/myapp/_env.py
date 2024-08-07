import jsons

from zrb import Env, EnvFile

from ._constant import (
    APP_TEMPLATE_ENV_FILE_NAME,
    DEPLOYMENT_DIR,
    DEPLOYMENT_TEMPLATE_ENV_FILE_NAME,
    MODULES,
)

app_env_file = EnvFile(path=APP_TEMPLATE_ENV_FILE_NAME, prefix="MYAPP")

app_enable_otel_env = Env(
    name="APP_ENABLE_OTEL",
    default='{{ "1" if input.enable_myapp_monitoring else "0" }}',
)

deployment_app_env_file = EnvFile(
    path=APP_TEMPLATE_ENV_FILE_NAME, prefix="DEPLOYMENT_APP_MYAPP"
)

deployment_config_env_file = EnvFile(
    path=DEPLOYMENT_TEMPLATE_ENV_FILE_NAME, prefix="DEPLOYMENT_CONFIG_MYAPP"
)

deployment_enable_monitoring_env = Env(
    name="ENABLE_MONITORING",
    os_name="DEPLOYMENT_CONFIG_MYAPP_ENABLE_MONITORING",
    default="{{ 1 if input.enable_myapp_monitoring else 0 }}",
)

pulumi_backend_url_env = Env(
    name="PULUMI_BACKEND_URL",
    os_name="PULUMI_MYAPP_BACKEND_URL",
    default=f"file://{DEPLOYMENT_DIR}/state",
)

pulumi_config_passphrase_env = Env(
    name="PULUMI_CONFIG_PASSPHRASE",
    os_name="PULUMI_MYAPP_CONFIG_PASSPHRASE",
    default="secret",
)

deployment_modules_env = Env(
    name="MODULES",
    os_name="DEPLOYMENT_CONFIG_MYAPP_MODULES",
    default=jsons.dumps(MODULES),
)

deployment_modules_env = Env(
    name="MODULES",
    os_name="DEPLOYMENT_CONFIG_MYAPP_MODULES",
    default=jsons.dumps(MODULES),
)
