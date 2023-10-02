from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.command.container.list import app__container__list
from addons.app.AppAddonManager import AppAddonManager
from src.helper.command import execute_command

from src.core.Kernel import Kernel
from src.decorator.command import command
from src.decorator.option import option

# Return true if config is set to started
APP_STARTED_CHECK_MODE_CONFIG = 'config'
# Return true if config is set to started and every container runs
APP_STARTED_CHECK_MODE_FULL = 'full'
# Return true if config is set to started and at least one container runs
APP_STARTED_CHECK_MODE_ANY_CONTAINER = 'any-container'


@command(help="Return true if app is started")
@app_dir_option()
@option('--mode', '-m', type=str, required=False, default=APP_STARTED_CHECK_MODE_FULL,
        help="Define how to define if app is started or not")
def app__app__started(kernel: Kernel, app_dir: str, mode: str = APP_STARTED_CHECK_MODE_FULL):
    if not kernel.addons['app'].get_runtime_config('started', False):
        return False

    manager: AppAddonManager = kernel.addons['app']
    if manager.runtime_docker_compose == {}:
        return False

    if mode == APP_STARTED_CHECK_MODE_CONFIG:
        return True

    container_names = kernel.run_function(
        app__container__list,
        {
            'app-dir': app_dir
        }
    ).first()

    # for container_name in list:
    running_containers = execute_command(
        kernel,
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
