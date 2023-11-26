from addons.app.command.container.list import app__container__list
from src.helper.command import execute_command

from src.decorator.option import option
from addons.app.decorator.app_command import app_command
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager

# Return true if config is set to started
APP_STARTED_CHECK_MODE_CONFIG = 'config'
# Return true if config is set to started and every container runs
APP_STARTED_CHECK_MODE_FULL = 'full'
# Return true if config is set to started and at least one container runs
APP_STARTED_CHECK_MODE_ANY_CONTAINER = 'any-container'


@app_command(help="Return true if app is started")
@option('--mode', '-m', type=str, required=False, default=APP_STARTED_CHECK_MODE_ANY_CONTAINER,
        help="Define how to define if app is started or not")
def app__app__started(manager: 'AppAddonManager', app_dir: str, mode: str = APP_STARTED_CHECK_MODE_ANY_CONTAINER):
    if not manager.get_runtime_config('started', False):
        return False

    if manager.runtime_docker_compose == {}:
        return False

    if mode == APP_STARTED_CHECK_MODE_CONFIG:
        return True

    container_names = manager.kernel.run_function(
        app__container__list,
        {
            'app-dir': app_dir
        }
    ).first()

    # for container_name in list:
    success, running_containers = execute_command(
        manager.kernel,
        ['docker', 'ps', '--format', '{{.Names}}']
    )

    all_runs: bool = True
    for name in container_names:
        if name in running_containers:
            if mode == APP_STARTED_CHECK_MODE_ANY_CONTAINER:
                return True
        else:
            all_runs: bool = False
            if mode == APP_STARTED_CHECK_MODE_FULL:
                return False

    # Every file is in place
    return all_runs
