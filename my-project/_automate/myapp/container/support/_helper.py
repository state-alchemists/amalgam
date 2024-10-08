from typing import Any

from zrb import Task


def activate_support_compose_profile(*args: Any, **kwargs: Any) -> str:
    compose_profiles = get_support_container_compose_profiles(*args, **kwargs)
    compose_profile_str = ",".join(compose_profiles)
    return f"export COMPOSE_PROFILES={compose_profile_str}"


def should_start_support_container(*args: Any, **kwargs: Any) -> bool:
    if not kwargs.get("local_myapp", True):
        return False
    compose_profiles = get_support_container_compose_profiles(*args, **kwargs)
    return len(compose_profiles) > 0


def get_support_container_compose_profiles(*args: Any, **kwargs: Any) -> list[str]:
    task: Task = kwargs.get("_task")
    env_map = task.get_env_map()
    compose_profiles: list[str] = []
    if env_map.get("APP_DB_CONNECTION", "").startswith("postgresql"):
        compose_profiles.append("postgres")
    broker_type = env_map.get("APP_BROKER_TYPE", "rabbitmq")
    if broker_type in ["rabbitmq", "kafka"]:
        compose_profiles.append(broker_type)
    if kwargs.get("enable_myapp_monitoring", False):
        compose_profiles.append("monitoring")
    return compose_profiles
