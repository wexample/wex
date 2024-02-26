import shutil
from typing import TYPE_CHECKING

from addons.app.const.app import APP_ENV_LOCAL, APP_ENVS
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE
from src.helper.service import service_copy_sample_dir

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Install service", command_type=COMMAND_TYPE_SERVICE)
def php__service__install(
    manager: "AppAddonManager", app_dir: str, service: str
) -> None:
    service_copy_sample_dir(manager.kernel, "php", "cron")

    # Install one "cron" file per environment
    cron_config_dir = manager.get_env_dir("cron", True)
    envs = APP_ENVS.copy()
    env = manager.get_env()

    if not env in envs:
        envs.append(env)

    for env_name in envs:
        if env_name != APP_ENV_LOCAL:
            shutil.copy2(f"{cron_config_dir}local", f"{cron_config_dir}{env_name}")
