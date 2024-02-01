import os.path
import time
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
    print(app_dir)
    print(manager._config)
    print(manager._runtime_config)

    if not manager.has_runtime_config("started"):
        print(' ZZZ A')
        manager.kernel.io.log(
            f"Runtime config file is missing", verbosity=VERBOSITY_LEVEL_MAXIMUM
        )
        return False

    started = manager.get_runtime_config("started").get_bool()
    if not started:
        print(' ZZZ B')
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
        print(' ZZZ D')
        manager.kernel.io.log(f"Config files exists", verbosity=VERBOSITY_LEVEL_MAXIMUM)
        return True
    print(' ZZZ E')
    container_names = manager.kernel.run_function(
        app__container__list, {"app-dir": app_dir}
    ).first()

    print(container_names)

    # for container_name in list:
    success, running_containers = execute_command_sync(
        manager.kernel, ["docker", "ps", "--format", "{{.Names}}"]
    )

    print(success)
    print(running_containers)

    all_runs: bool = True
    for name in container_names:
        print(' ZZZ F' + name)
        if name in running_containers:
            print(' ZZZ G')
            manager.kernel.io.log(
                f"Container {name} runs", verbosity=VERBOSITY_LEVEL_MAXIMUM
            )
            if mode == APP_STARTED_CHECK_MODE_ANY_CONTAINER:
                print(' ZZZ GG')
                return True
        else:
            print(' ZZZ H')
            all_runs = False
            manager.kernel.io.log(
                f"Container {name} does not run", verbosity=VERBOSITY_LEVEL_MAXIMUM
            )
            if mode == APP_STARTED_CHECK_MODE_FULL:
                print(' ZZZ HH')
                return False
    print(' ZZZ I')
    # Every file is in place
    return all_runs
