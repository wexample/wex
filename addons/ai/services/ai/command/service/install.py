from typing import TYPE_CHECKING

from wexample_helpers_yaml.helpers.yaml_helpers import yaml_read, yaml_write

from addons.app.decorator.app_command import app_command
from addons.app.helper.docker import DOCKER_COMPOSE_REL_PATH_BASE
from src.helper.service import service_copy_sample_dir
from src.const.globals import COMMAND_TYPE_SERVICE

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Install the ai service", command_type=COMMAND_TYPE_SERVICE)
def ai__service__install(
    manager: "AppAddonManager", app_dir: str, service: str
) -> None:
    docker_config_path = manager.get_env_dir() + DOCKER_COMPOSE_REL_PATH_BASE
    docker_config = yaml_read(docker_config_path)

    key = f"{manager.get_app_name()}_postgres"
    docker_config["services"][key] = (
        docker_config["services"][key] if key in docker_config["services"] else {}
    )
    docker_config["services"][key]["ports"] = [
        f"5{manager.get_config('port.public', 444).get_int()}:5432"
    ]

    # Override postgres with pgvector image.
    docker_config["services"][key][
        "image"
    ] = "gitlab-docker.wexample.com/wexample-public/docker/pgvector:latest"

    yaml_write(docker_config_path, docker_config)

    service_copy_sample_dir(
        manager.kernel,
        service,
        "postgres/dumps"
    )
