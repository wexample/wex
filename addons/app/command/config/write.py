import os
from typing import TYPE_CHECKING, Optional

import yaml

from addons.app.command.hook.exec import app__hook__exec
from addons.app.const.app import APP_FILEPATH_REL_COMPOSE_RUNTIME_YML
from addons.app.decorator.app_command import app_command
from addons.app.helper.docker import (
    docker_exec_app_compose,
    docker_get_app_compose_files,
)
from src.helper.prompt import prompt_progress_steps
from src.decorator.option import option

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(
    help="Write the configuration file for services to start", should_be_valid=True
)
@option("--user", "-u", type=str, required=False, help="Owner of application files")
@option("--group", "-g", type=str, required=False, help="Group of application files")
def app__config__write(
    manager: "AppAddonManager",
    app_dir: str,
    user: Optional[str] = None,
    group: Optional[str] = None,
) -> None:
    kernel = manager.kernel

    def _app__config__write__runtime() -> None:
        nonlocal user
        nonlocal group

        manager.build_runtime_config(user, group)

    def _app__config__write__docker() -> None:
        kernel.run_function(
            app__hook__exec, {"app-dir": app_dir, "hook": "config/write-compose-pre"}
        )

        compose_files = docker_get_app_compose_files(manager, app_dir)

        if not len(compose_files) != 0:
            manager.log("No docker compose file")
            return

        manager.log(f"Compiling docker compose file...")
        yml_content = str(
            docker_exec_app_compose(kernel, app_dir, compose_files, "config")
        )

        try:
            yaml.safe_load(yml_content)
        except yaml.YAMLError:
            kernel.io.print(yml_content)

            kernel.io.error("Wrong yaml from docker compose")

        with open(
            os.path.join(app_dir, APP_FILEPATH_REL_COMPOSE_RUNTIME_YML), "w"
        ) as f:
            f.write(yml_content)

        kernel.run_function(
            app__hook__exec, {"app-dir": app_dir, "hook": "config/write-post"}
        )

    prompt_progress_steps(
        kernel,
        [
            _app__config__write__runtime,
            _app__config__write__docker,
        ],
    )
