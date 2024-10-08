from typing import Any

from ..support._helper import get_support_container_compose_profiles


def activate_monolith_compose_profile(*args: Any, **kwargs: Any) -> str:
    compose_profiles = _get_monolith_container_compose_profiles(*args, **kwargs)
    compose_profile_str = ",".join(compose_profiles)
    return f"export COMPOSE_PROFILES={compose_profile_str}"


def should_start_monolith_container(*args: Any, **kwargs: Any) -> bool:
    if not kwargs.get("local_myapp", True):
        return False
    compose_profiles = _get_monolith_container_compose_profiles(*args, **kwargs)
    return len(compose_profiles) > 0


def _get_monolith_container_compose_profiles(*args: Any, **kwargs: Any) -> list[str]:
    compose_profiles = get_support_container_compose_profiles(*args, **kwargs)
    compose_profiles.append("monolith")
    return compose_profiles
