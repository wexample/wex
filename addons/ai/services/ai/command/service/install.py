from typing import TYPE_CHECKING, cast

from addons.app.decorator.app_command import app_command
from addons.app.helper.docker import DOCKER_COMPOSE_REL_PATH_BASE
from wexample_helpers.const.types import StringKeysDict
from src.const.globals import COMMAND_TYPE_SERVICE
from src.helper.service import service_copy_sample_dir
from wexample_helpers_yaml.helpers.yaml_helpers import yaml_read, yaml_write

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Install the ai service", command_type=COMMAND_TYPE_SERVICE)
def ai__service__install(
        manager: "AppAddonManager", app_dir: str, service: str
) -> None:
    docker_config_path = manager.get_env_dir() + DOCKER_COMPOSE_REL_PATH_BASE
    # yaml_read returns a StructuredData union. Cast to a dict for typed indexing.
    docker_config = cast(StringKeysDict, yaml_read(docker_config_path) or {})

    # Ensure services is a mutable dict
    services = cast(StringKeysDict, docker_config.get("services") or {})
    docker_config["services"] = services

    key = f"{manager.get_app_name()}_postgres"
    service_entry = cast(StringKeysDict, services.get(key) or {})
    services[key] = service_entry

    service_entry["ports"] = [
        f"5{manager.get_config('port.public', 444).get_int()}:5432"
    ]

    # Override postgres with pgvector image.
    service_entry["image"] = (
        "gitlab-docker.wexample.com/wexample-public/docker/pgvector:latest"
    )

    yaml_write(docker_config_path, docker_config)

    service_copy_sample_dir(
        manager.kernel,
        service,
        "postgres/dumps"
    )
