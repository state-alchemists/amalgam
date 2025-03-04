import os

from zrb import AnyContext, Task, make_task

from myapp._zrb.column.add_column_util import (
    update_myapp_schema,
    update_myapp_test_create,
    update_myapp_test_delete,
    update_myapp_test_read,
    update_myapp_test_update,
    update_myapp_ui,
)
from myapp._zrb.config import APP_DIR
from myapp._zrb.format_task import format_myapp_code
from myapp._zrb.group import app_create_group
from myapp._zrb.input import (
    existing_entity_input,
    existing_module_input,
    new_column_input,
    new_column_type_input,
)
from myapp._zrb.util import get_existing_module_names, get_existing_schema_names


@make_task(
    name="validate-add-myapp-column",
    input=[
        existing_module_input,
        existing_entity_input,
    ],
    retries=0,
)
async def validate_add_myapp_column(ctx: AnyContext):
    module_name = ctx.input.module
    if module_name not in get_existing_module_names():
        raise ValueError(f"Module not exist: {module_name}")
    schema_name = ctx.input.entity
    if schema_name not in get_existing_schema_names():
        raise ValueError(f"Schema not exist: {schema_name}")


update_myapp_schema_task = Task(
    name="update-myapp-schema",
    input=[
        existing_module_input,
        existing_entity_input,
        new_column_input,
        new_column_type_input,
    ],
    action=update_myapp_schema,
    retries=0,
    upstream=validate_add_myapp_column,
)

update_myapp_ui_task = Task(
    name="update-myapp-ui",
    input=[
        existing_module_input,
        existing_entity_input,
        new_column_input,
        new_column_type_input,
    ],
    action=update_myapp_ui,
    retries=0,
    upstream=validate_add_myapp_column,
)

update_myapp_test_create_task = Task(
    name="update-myapp-test-create",
    input=[
        existing_module_input,
        existing_entity_input,
        new_column_input,
        new_column_type_input,
    ],
    action=update_myapp_test_create,
    retries=0,
    upstream=validate_add_myapp_column,
)

update_myapp_test_read_task = Task(
    name="update-myapp-test-read",
    input=[
        existing_module_input,
        existing_entity_input,
        new_column_input,
        new_column_type_input,
    ],
    action=update_myapp_test_read,
    retries=0,
    upstream=validate_add_myapp_column,
)

update_myapp_test_update_task = Task(
    name="update-myapp-test-update",
    input=[
        existing_module_input,
        existing_entity_input,
        new_column_input,
        new_column_type_input,
    ],
    action=update_myapp_test_update,
    retries=0,
    upstream=validate_add_myapp_column,
)

update_myapp_test_delete_task = Task(
    name="update-myapp-test-delete",
    input=[
        existing_module_input,
        existing_entity_input,
        new_column_input,
        new_column_type_input,
    ],
    action=update_myapp_test_delete,
    retries=0,
    upstream=validate_add_myapp_column,
)


add_myapp_column = app_create_group.add_task(
    Task(
        name="add-myapp-column",
        description="📊 Create new column on an entity",
        upstream=[
            update_myapp_schema_task,
            update_myapp_ui_task,
            update_myapp_test_create_task,
            update_myapp_test_read_task,
            update_myapp_test_update_task,
            update_myapp_test_delete_task,
        ],
        successor=format_myapp_code,
        retries=0,
    ),
    alias="column",
)
