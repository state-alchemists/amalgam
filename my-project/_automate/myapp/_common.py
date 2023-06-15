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
SKIP_CONTAINER_EXECUTION = '{{not input.local_myapp}}'
SKIP_SUPPORT_CONTAINER_EXECUTION = ' '.join([
    '{{',
    'not input.local_myapp',
    'or env.get("APP_BROKER_TYPE") not in ["rabbitmq", "kafka"]',
    '}}',
])
SKIP_LOCAL_MONOLITH_EXECUTION = ' '.join([
    '{{',
    'not input.local_myapp',
    'or input.myapp_run_mode == "microservices"',
    '}}',
])
SKIP_LOCAL_MICROSERVICES_EXECUTION = ' '.join([
    '{{',
    'not input.local_myapp',
    'or input.myapp_run_mode == "monolith"',
    '}}',
])

MODULE_CONFIG_PATH = os.path.join(CURRENT_DIR, 'config', 'modules.json')
with open(MODULE_CONFIG_PATH) as file:
    MODULE_JSON_STR = file.read()
MODULES = jsons.loads(MODULE_JSON_STR)


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
    port='{{env.get("KAFKA_PLAINTEXT_HOST_PORT", "29092")}}',
    skip_execution='{{env.get("APP_BROKER_TYPE", "rabbitmq") != "kafka"}}'
)

kafka_outside_checker = PortChecker(
    name='check-kafka-outside',
    port='{{env.get("KAFKA_OUTSIDE_HOST_PORT", "9092")}}',
    skip_execution='{{env.get("APP_BROKER_TYPE", "rabbitmq") != "kafka"}}'
)

pandaproxy_plaintext_checker = PortChecker(
    name='check-pandaproxy-plaintext',
    port='{{env.get("PANDAPROXY_PLAINTEXT_HOST_PORT", "29092")}}',
    skip_execution='{{env.get("APP_BROKER_TYPE", "rabbitmq") != "kafka"}}'
)

pandaproxy_outside_checker = PortChecker(
    name='check-pandaproxy-outside',
    port='{{env.get("PANDAPROXY_OUTSIDE_HOST_PORT", "9092")}}',
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
    skip_execution=SKIP_LOCAL_MICROSERVICES_EXECUTION
)

###############################################################################
# Input Definitions
###############################################################################

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
# Env file Definitions
###############################################################################

###############################################################################
# Env fDefinitions
###############################################################################

local_app_port_env = Env(
    name='APP_PORT',
    os_name='MYAPP_APP_PORT',
    default='3000'
)

local_app_broker_type_env = Env(
    name='APP_BROKER_TYPE',
    os_name='MYAPP_APP_BROKER_TYPE',
    default='rabbitmq'
)
