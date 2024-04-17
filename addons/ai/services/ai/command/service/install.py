from typing import TYPE_CHECKING

from addons.app.decorator.app_command import app_command
from addons.app.helper.docker import DOCKER_COMPOSE_REL_PATH_BASE
from src.const.globals import COMMAND_TYPE_SERVICE
from src.helper.data_yaml import yaml_load, yaml_write

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Install the ai service", command_type=COMMAND_TYPE_SERVICE)
def ai__service__install(
    manager: "AppAddonManager",
    app_dir: str,
    service: str
) -> None:
    docker_config_path = manager.get_env_dir() + DOCKER_COMPOSE_REL_PATH_BASE
    docker_config = yaml_load(docker_config_path)
    docker_config["services"]["wex_ai_postgres"] = {"ports": ["5444:5432"]}

    yaml_write(
        docker_config_path,
        docker_config
    )
