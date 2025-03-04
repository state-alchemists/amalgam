from zrb import Group
from zrb.builtin.group import project_group

app_group = project_group.add_group(
    Group(name="myapp", description="🚀 Managing Myapp")
)

app_run_group = app_group.add_group(Group(name="run", description="🟢 Run Myapp"))

app_migrate_group = app_group.add_group(
    Group(name="migrate", description="📦 Run Myapp DB migration")
)

app_create_group = app_group.add_group(
    Group(name="create", description="✨ Create resources for Myapp")
)

app_create_migration_group = app_create_group.add_group(
    Group(name="migration", description="📦 Create Myapp DB migration")
)
