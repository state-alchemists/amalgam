import os

from zrb import BoolInput, IntInput, StrInput

local_input = BoolInput(
    name="local-myapp",
    description='Use "myapp" on local machine',
    prompt='Use "myapp" on local machine?',
    default=True,
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

replica_input = IntInput(
    name="myapp-replica",
    description='Replica of "myapp"',
    prompt='Replica of "myapp"',
    default=1,
)

pulumi_stack_input = StrInput(
    name="myapp-pulumi-stack",
    description='Pulumi stack name for "myapp"',
    prompt='Pulumi stack name for "myapp"',
    default=os.getenv("ZRB_ENV", "dev"),
)
