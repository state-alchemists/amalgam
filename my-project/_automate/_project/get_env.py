from typing import Any

from zrb import BoolInput, python_task, runner
from zrb.builtin import project_group
from zrb.helper.env_map.fetch import fetch_env_map_from_group


@python_task(
    name="get-env",
    description="Get default values for project environments",
    inputs=[
        BoolInput(
            name="export",
            shortcut="e",
            description="Whether add export statement or not",
            default=True,
        )
    ],
    group=project_group,
    runner=runner,
)
async def get_project_env(*args: Any, **kwargs: Any) -> str:
    env_map: Mapping[str, str] = {}
    env_map = fetch_env_map_from_group(env_map, project_group)
    env_keys = list(env_map.keys())
    env_keys.sort()
    should_export = kwargs.get("export", True)
    export_prefix = "export " if should_export else ""
    return "\n".join([f"{export_prefix}{key}={env_map[key]}" for key in env_keys])
