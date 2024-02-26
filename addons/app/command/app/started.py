from typing import TYPE_CHECKING

from addons.app.command.container.list import app__container__list
from addons.app.decorator.app_command import app_command
from src.const.globals import VERBOSITY_LEVEL_MAXIMUM
from src.decorator.option import option
from src.helper.command import execute_command_sync

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager

# Return true if config is set to started
APP_STARTED_CHECK_MODE_CONFIG = "config"
# Return true if config is set to started and every container runs
APP_STARTED_CHECK_MODE_FULL = "full"
# Return true if config is set to started and at least one container runs
APP_STARTED_CHECK_MODE_ANY_CONTAINER = "any-container"


@app_command(help="Return true if app is started")
@option(
    "--mode",
    "-m",
    type=str,
    required=False,
    default=APP_STARTED_CHECK_MODE_ANY_CONTAINER,
    help="Define how to define if app is started or not",
)
def app__app__started(
    manager: "AppAddonManager",
    app_dir: str,
    mode: str = APP_STARTED_CHECK_MODE_ANY_CONTAINER,
) -> bool:
    if manager.require_proxy() and not manager.has_proxy_app():
        manager.kernel.io.log(
            f"App is not registered in proxy of env [{manager.get_env()}]",
            verbosity=VERBOSITY_LEVEL_MAXIMUM,
        )
        return False

    if not manager.has_runtime_config("started"):
        manager.kernel.io.log(
            f"Runtime config file is missing", verbosity=VERBOSITY_LEVEL_MAXIMUM
        )
        return False

    started = manager.get_runtime_config("started").get_bool()
    if not started:
        manager.kernel.io.log(
            f"Runtime config is marked as stopped", verbosity=VERBOSITY_LEVEL_MAXIMUM
        )
        return False

    if not manager.runtime_docker_compose:
        manager.kernel.io.log(
            f"Runtime docker config is missing", verbosity=VERBOSITY_LEVEL_MAXIMUM
        )
        return False

    if mode == APP_STARTED_CHECK_MODE_CONFIG:
        manager.kernel.io.log(f"Config files exists", verbosity=VERBOSITY_LEVEL_MAXIMUM)
        return True

    container_names = manager.kernel.run_function(
        app__container__list, {"app-dir": app_dir}
    ).first()

    # for container_name in list:
    success, running_containers = execute_command_sync(
        manager.kernel, ["docker", "ps", "--format", "{{.Names}}"]
    )

    all_runs: bool = True
    for name in container_names:
        if name in running_containers:
            manager.kernel.io.log(
                f"Container {name} runs", verbosity=VERBOSITY_LEVEL_MAXIMUM
            )
            if mode == APP_STARTED_CHECK_MODE_ANY_CONTAINER:
                return True
        else:
            all_runs = False
            manager.kernel.io.log(
                f"Container {name} does not run", verbosity=VERBOSITY_LEVEL_MAXIMUM
            )
            if mode == APP_STARTED_CHECK_MODE_FULL:
                return False

    # Every file is in place
    return all_runs
