import os

from zrb import AnyContext, ContentTransformer, Scaffolder, Task, make_task

from myapp._zrb.config import APP_DIR
from myapp._zrb.format_task import format_myapp_code
from myapp._zrb.group import app_create_group
from myapp._zrb.input import new_module_input
from myapp._zrb.module.add_module_util import (
    is_app_config_file,
    is_app_main_file,
    is_app_zrb_config_file,
    is_app_zrb_task_file,
    is_gateway_module_subroute_file,
    is_gateway_navigation_config_file,
    is_gateway_route_file,
    is_in_module_dir,
    update_app_config_file,
    update_app_main_file,
    update_app_zrb_config_file,
    update_app_zrb_task_file,
    update_gateway_navigation_config_file,
    update_gateway_route_file,
)
from myapp._zrb.util import get_existing_module_names


@make_task(
    name="validate-add-myapp-module",
    input=new_module_input,
    retries=0,
)
async def validate_add_myapp_module(ctx: AnyContext):
    if ctx.input.module in get_existing_module_names():
        raise ValueError(f"Module already exists: {ctx.input.module}")


scaffold_myapp_module = Scaffolder(
    name="scaffold-myapp-module",
    input=new_module_input,
    source_path=os.path.join(os.path.dirname(__file__), "template", "app_template"),
    render_source_path=False,
    destination_path=APP_DIR,
    transform_path={
        "my_module": "{to_snake_case(ctx.input.module)}",
    },
    transform_content=[
        # Common transformation (myapp/module/snake_module_name)
        ContentTransformer(
            name="transform-module-dir",
            match=is_in_module_dir,
            transform={
                "MY_MODULE": "{to_snake_case(ctx.input.module).upper()}",
                "my_module": "{to_snake_case(ctx.input.module)}",
                "MyModule": "{to_pascal_case(ctx.input.module)}",
            },
        ),
        # Gateway's module subroute (myapp/module/gateway/subroute/snake_module_name.py)
        ContentTransformer(
            name="transform-gateway-subroute",
            match=is_gateway_module_subroute_file,
            transform={
                "my_module": "{to_snake_case(ctx.input.module)}",
            },
        ),
        # Register module config to myapp/config.py
        ContentTransformer(
            name="transform-app-config",
            match=is_app_config_file,
            transform=update_app_config_file,
        ),
        # Register module route to myapp/main.py
        ContentTransformer(
            name="transform-app-main",
            match=is_app_main_file,
            transform=update_app_main_file,
        ),
        # Register module's tasks to myapp/_zrb/task.py
        ContentTransformer(
            name="transform-zrb-task",
            match=is_app_zrb_task_file,
            transform=update_app_zrb_task_file,
        ),
        # Register module's base url to myapp/_zrb/config.py
        ContentTransformer(
            name="transform-zrb-config",
            match=is_app_zrb_config_file,
            transform=update_app_zrb_config_file,
        ),
        # Register module's subroute to myapp/gateway/route.py
        ContentTransformer(
            name="transform-gateway-route",
            match=is_gateway_route_file,
            transform=update_gateway_route_file,
        ),
        # Register module's page to myapp/gateway/config/navigation.py
        ContentTransformer(
            name="transform-gateway-navigation-config",
            match=is_gateway_navigation_config_file,
            transform=update_gateway_navigation_config_file,
        ),
    ],
    retries=0,
    upstream=validate_add_myapp_module,
)

add_myapp_module = app_create_group.add_task(
    Task(
        name="add-myapp-module",
        description="🧩 Create new module on Myapp",
        upstream=scaffold_myapp_module,
        successor=format_myapp_code,
        retries=0,
    ),
    alias="module",
)
