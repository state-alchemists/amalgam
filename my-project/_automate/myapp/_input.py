import os

from zrb import BoolInput, ChoiceInput, StrInput

enable_monitoring_input = BoolInput(
    name="enable-myapp-monitoring",
    description='Enable "myapp" monitoring',
    prompt='Enable "myapp" monitoring?',
    default=False,
)

local_input = BoolInput(
    name="local-myapp",
    description='Use "myapp" on local machine',
    prompt='Use "myapp" on local machine?',
    default=True,
)

run_mode_input = ChoiceInput(
    name="myapp-run-mode",
    description='"myapp" run mode (monolith/microservices)',
    prompt='Run "myapp" as a monolith or microservices?',
    choices=["monolith", "microservices"],
    default="monolith",
)

https_input = BoolInput(
    name="myapp-https",
    description='Whether "myapp" run on HTTPS',
    prompt='Is "myapp" run on HTTPS?',
    default=False,
)

host_input = StrInput(
    name="myapp-host",
    description='Hostname of "myapp"',
    prompt='Hostname of "myapp"',
    default="localhost",
)

image_input = StrInput(
    name="myapp-image",
    description='Image name of "myapp"',
    prompt='Image name of "myapp"',
    default="docker.io/gofrendi/myapp:latest",
)

deploy_mode_input = ChoiceInput(
    name="myapp-deploy-mode",
    description='"myapp" deploy mode (monolith/microservices)',
    prompt='Deploy "myapp" as a monolith or microservices?',
    choices=["monolith", "microservices"],
    default="monolith",
)

pulumi_stack_input = StrInput(
    name="myapp-pulumi-stack",
    description='Pulumi stack name for "myapp"',
    prompt='Pulumi stack name for "myapp"',
    default=os.getenv("ZRB_ENV", "dev"),
)
