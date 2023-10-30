import getpass
import os.path

from addons.app.command.app.init import app__app__init
from addons.app.command.env.get import app__env__get
from addons.app.command.app.started import app__app__started
from addons.app.command.app.start import app__app__start
from src.const.error import ERR_UNEXPECTED
from src.helper.system import get_processes_by_port
from src.decorator.as_sudo import as_sudo
from addons.app.AppAddonManager import AppAddonManager
from src.core.Kernel import Kernel
from src.decorator.command import command
from src.decorator.option import option
from src.core.response.ResponseCollectionResponse import ResponseCollectionResponse
from src.core.response.ResponseCollectionStopResponse import ResponseCollectionStopResponse


@command(help="Create and start the reverse proxy server")
@as_sudo
@option('--user', '-u', type=str, required=False, help="Owner of application files")
@option('--env', '-e', type=str, required=False, help="Env for accessing apps")
@option('--group', '-g', type=str, required=False, help="Group of application files")
@option('--port', '-p', type=int, required=False, help="Port for web server")
@option('--port-secure', '-ps', type=int, required=False, help="Secure port for web server")
def app__proxy__start(kernel: Kernel,
                      env: str = None,
                      user: str = None,
                      group: str = None,
                      port: str = None,
                      port_secure: str = None
                      ):
    manager: AppAddonManager = kernel.addons['app']
    proxy_path = manager.get_proxy_path()

    def _app__proxy__start__create():
        manager.log('Starting proxy server')

        # Created
        if manager.is_app_root(proxy_path):
            # Started
            if kernel.run_function(app__app__started, {
                'app-dir': proxy_path,
            }).first():
                return ResponseCollectionStopResponse(kernel)
        else:
            manager.log(f'Creating proxy dir {proxy_path}')
            os.makedirs(
                proxy_path,
                exist_ok=True
            )

            kernel.run_function(
                app__app__init,
                {
                    'app-dir': proxy_path,
                    'services': ['proxy'],
                    'git': False
                }
            )

    def _app__proxy__start__checkup(previous):
        nonlocal user
        current_dir = os.getcwd()

        manager.set_app_workdir(proxy_path)

        user = user or getpass.getuser()

        def check_port(port_to_check: int):
            if not port_to_check:
                kernel.io.error(
                    ERR_UNEXPECTED,
                    {
                        'error': f"Invalid port {port_to_check}"
                    }
                )

            manager.log(f'Checking that port {port_to_check} is free')

            # Check port availability.
            process = get_processes_by_port(port_to_check)
            if process:
                kernel.io.error(
                    ERR_UNEXPECTED,
                    {
                        'error': f"Process {process.pid} ({process.name()}) is using port {port_to_check}"
                    }
                )

            kernel.io.success(f'Port {port_to_check} free')

        check_port(
            manager.get_config('global.port_public')
        )
        check_port(
            manager.get_config('global.port_public_secure')
        )

        manager.unset_app_workdir(current_dir)

    def _app__proxy__start__start(previous):
        return kernel.run_function(
            app__app__start,
            {
                'app-dir': proxy_path,
                # If no env, use the global wex env.
                'env': env or kernel.run_function(
                    app__env__get,
                    {
                        'app-dir': kernel.get_path('root')
                    }
                ).first(),
                'user': user,
                'group': group,
            }
        )

    return ResponseCollectionResponse(kernel, [
        _app__proxy__start__create,
        _app__proxy__start__checkup,
        _app__proxy__start__start,
    ])
