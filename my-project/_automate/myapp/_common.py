from typing import Any
from zrb import (
    BoolInput, ChoiceInput, StrInput, Env, HTTPChecker, PortChecker
)
import jsons
import os

###############################################################################
# Constants
###############################################################################

CURRENT_DIR = os.path.dirname(__file__)
PROJECT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..', '..'))
RESOURCE_DIR = os.path.join(PROJECT_DIR, 'src', 'myapp')
DEPLOYMENT_DIR = os.path.join(RESOURCE_DIR, 'deployment')
DEPLOYMENT_TEMPLATE_ENV_FILE_NAME = os.path.join(
    DEPLOYMENT_DIR, 'template.env'
)
APP_DIR = os.path.join(RESOURCE_DIR, 'src')
APP_FRONTEND_DIR = os.path.join(APP_DIR, 'frontend')
APP_FRONTEND_BUILD_DIR = os.path.join(APP_FRONTEND_DIR, 'build')
APP_TEMPLATE_ENV_FILE_NAME = os.path.join(APP_DIR, 'template.env')
MODULE_CONFIG_PATH = os.path.join(CURRENT_DIR, 'config', 'modules.json')
with open(MODULE_CONFIG_PATH) as file:
    MODULE_JSON_STR = file.read()
MODULES = jsons.loads(MODULE_JSON_STR)

###############################################################################
# Functions
###############################################################################


def skip_local_microservices_execution(*args: Any, **kwargs: Any) -> bool:
    if not kwargs.get('local_myapp', True):
        return True
    run_mode = kwargs.get('myapp_run_mode', 'monolith')
    return run_mode != 'microservices'


###############################################################################
# Checker Task Definitions
###############################################################################

rabbitmq_management_checker = HTTPChecker(
    name='check-rabbitmq-management',
    port='{{env.get("RABBITMQ_MANAGEMENT_HOST_PORT", "15672")}}',
    is_https='{{input.myapp_https}}',
    skip_execution='{{env.get("APP_BROKER_TYPE", "rabbitmq") != "rabbitmq"}}'
)

rabbitmq_checker = PortChecker(
    name='check-rabbitmq',
    port='{{env.get("RABBITMQ_HOST_PORT", "5672")}}',
    skip_execution='{{env.get("APP_BROKER_TYPE", "rabbitmq") != "rabbitmq"}}'
)

redpanda_console_checker = HTTPChecker(
    name='check-redpanda-console',
    method='GET',
    port='{{env.get("REDPANDA_CONSOLE_HOST_PORT", "9000")}}',
    is_https='{{input.myapp_https}}',
    skip_execution='{{env.get("APP_BROKER_TYPE", "rabbitmq") != "kafka"}}'
)

kafka_plaintext_checker = PortChecker(
    name='check-kafka-plaintext',
    port='{{env.get("KAFKA_INTERNAL_HOST_PORT", "29092")}}',
    skip_execution='{{env.get("APP_BROKER_TYPE", "rabbitmq") != "kafka"}}'
)

kafka_outside_checker = PortChecker(
    name='check-kafka-outside',
    port='{{env.get("KAFKA_EXTERNAL_HOST_PORT", "9092")}}',
    skip_execution='{{env.get("APP_BROKER_TYPE", "rabbitmq") != "kafka"}}'
)

pandaproxy_plaintext_checker = PortChecker(
    name='check-pandaproxy-plaintext',
    port='{{env.get("PANDAPROXY_INTERNAL_HOST_PORT", "29092")}}',
    skip_execution='{{env.get("APP_BROKER_TYPE", "rabbitmq") != "kafka"}}'
)

pandaproxy_outside_checker = PortChecker(
    name='check-pandaproxy-outside',
    port='{{env.get("PANDAPROXY_EXTERNAL_HOST_PORT", "9092")}}',
    skip_execution='{{env.get("APP_BROKER_TYPE", "rabbitmq") != "kafka"}}'
)

app_container_checker = HTTPChecker(
    name='check-myapp-container',
    host='{{input.myapp_host}}',
    url='/readiness',
    port='{{env.get("HOST_PORT", "3000")}}',
    is_https='{{input.myapp_https}}'
)

app_local_checker = HTTPChecker(
    name='check-myapp',
    host='{{input.myapp_host}}',
    url='/readiness',
    port='{{env.APP_PORT}}',
    is_https='{{input.myapp_https}}',
    skip_execution=skip_local_microservices_execution
)

###############################################################################
# Input Definitions
###############################################################################

enable_monitoring_input = BoolInput(
    name='enable-myapp-monitoring',
    description='Enable "myapp" monitoring',
    prompt='Enable "myapp" monitoring?',
    default=False
)

local_input = BoolInput(
    name='local-myapp',
    description='Use "myapp" on local machine',
    prompt='Use "myapp" on local machine?',
    default=True
)

run_mode_input = ChoiceInput(
    name='myapp-run-mode',
    description='"myapp" run mode (monolith/microservices)',
    prompt='Run "myapp" as a monolith or microservices?',
    choices=['monolith', 'microservices'],
    default='monolith'
)

https_input = BoolInput(
    name='myapp-https',
    description='Whether "myapp" run on HTTPS',
    prompt='Is "myapp" run on HTTPS?',
    default=False
)

host_input = StrInput(
    name='myapp-host',
    description='Hostname of "myapp"',
    prompt='Hostname of "myapp"',
    default='localhost'
)

###############################################################################
# Env fDefinitions
###############################################################################

app_enable_otel_env = Env(
    name='APP_ENABLE_OTEL',
    default='{{ "1" if input.enable_myapp_monitoring else "0" }}'
)
