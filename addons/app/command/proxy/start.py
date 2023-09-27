import getpass
import os.path

from addons.app.command.app.init import app__app__init
from addons.app.command.env.get import app__env__get
from addons.app.const.app import APP_FILEPATH_REL_CONFIG
from addons.app.decorator.app_dir_ignore import app_dir_ignore
from addons.app.command.app.started import app__app__started, APP_STARTED_CHECK_MODE_CONFIG
from addons.app.command.app.start import app__app__start
from src.const.error import ERR_UNEXPECTED
from src.helper.system import get_processes_by_port
from src.decorator.as_sudo import as_sudo
from addons.app.AppAddonManager import AppAddonManager
from src.core.Kernel import Kernel
from src.decorator.command import command
from src.decorator.option import option


@command(help="Create and start the reverse proxy server")
@as_sudo
@app_dir_ignore
@option('--user', '-u', type=str, required=False, help="Owner of application files")
@option('--env', '-e', type=str, required=False, help="Port for accessing apps")
@option('--group', '-g', type=str, required=False, help="Group of application files")
@option('--port', '-p', type=int, required=False, help="Port for web server")
@option('--port-secure', '-ps', type=int, required=False, help="Secure port for web server")
def app__proxy__start(kernel: Kernel,
                      env: str = None,
                      user: str = None,
                      group: str = None,
                      port: str = None,
                      port_secure: str = None):
    manager: AppAddonManager = kernel.addons['app']

    current_dir = os.getcwd()

    # Created
    if manager.is_app_root(manager.proxy_path):
        if os.path.exists(APP_FILEPATH_REL_CONFIG):
            # Started
            if kernel.run_function(app__app__started, {
                'app-dir': manager.proxy_path,
                'check-mode': APP_STARTED_CHECK_MODE_CONFIG
            }):
                return
    else:
        kernel.log(f'Creating proxy dir {manager.proxy_path}')
        os.makedirs(
            manager.proxy_path,
            exist_ok=True
        )

        kernel.run_function(
            app__app__init,
            {
                'app-dir': manager.proxy_path,
                'services': ['proxy'],
                'git': False
            }
        )

    manager: AppAddonManager = kernel.addons['app']
    manager.set_app_workdir(manager.proxy_path)

    user = user or getpass.getuser()

    def check_port(port_to_check: int):
        if not port_to_check:
            kernel.error(
                ERR_UNEXPECTED,
                {
                    'error': f"Invalid port {port_to_check}"
                }
            )

        manager.log(f'Checking that port {port_to_check} is free')

        # Check port availability.
        process = get_processes_by_port(port_to_check)
        if process:
            kernel.error(
                ERR_UNEXPECTED,
                {
                    'error': f"Process {process.pid} ({process.name()}) is using port {port_to_check}"
                }
            )

    check_port(
        manager.get_config('global.port_public')
    )
    check_port(
        manager.get_config('global.port_public_secure')
    )

    manager.unset_app_workdir(current_dir)

    kernel.run_function(
        app__app__start,
        {
            'app-dir': manager.proxy_path,
            # If no env, use the global wex env.
            'env': env or app__env__get.callback(app_dir=kernel.path['root']),
            'user': user,
            'group': group,
        }
    )
