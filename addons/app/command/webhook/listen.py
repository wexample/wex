import shutil

from addons.system.command.system.is_docker import system__system__is_docker
from src.helper.command import execute_command
from src.const.globals import SYSTEM_SERVICES_PATH, SERVICE_DAEMON_NAME, SERVICE_DAEMON_PATH, COMMAND_TYPE_ADDON
from src.helper.core import get_daemon_service_resource_path
from src.helper.file import remove_file_if_exists
from src.helper.system import is_port_open, kill_process_by_port, kill_process_by_command, service_exec, \
    service_daemon_reload
from src.const.error import ERR_UNEXPECTED
from addons.app.WebhookHttpRequestHandler import WebhookHttpRequestHandler
from src.decorator.as_sudo import as_sudo
from http.server import HTTPServer
from src.core.Kernel import Kernel
from src.decorator.command import command
from src.decorator.option import option


@command(help="Serve webhook listener daemon")
@as_sudo
@option('--port', '-p', type=int, required=False, default=4242,
        help="Which port is used by service to listen incoming webhooks")
@option('--dry-run', '-dr', type=bool, required=False, default=False, is_flag=True,
        help="Do not start real service, useful for testing")
@option('--asynchronous', '-a', type=bool, required=False, default=False, is_flag=True,
        help="Use a daemon or not. Can't use daemon in a docker container")
@option('--force', '-f', type=bool, required=False, default=False, is_flag=True,
        help="Kill existing process if already running")
def app__webhook__listen(
        base_kernel: Kernel,
        port: int = 4242,
        dry_run: bool = False,
        asynchronous: bool = False,
        force: bool = False
):
    if is_port_open(port):
        if force:
            base_kernel.io.log(f'Port already in use {port}, killing process...')
            kill_process_by_port(port)
        else:
            base_kernel.io.error(ERR_UNEXPECTED, {
                'error': f'Port already in use {port}',
            })
            return False

    # Remove old service file
    remove_file_if_exists(SERVICE_DAEMON_PATH)

    if asynchronous:
        use_daemon = not base_kernel.run_function(system__system__is_docker)

        if use_daemon:
            daemon_path = get_daemon_service_resource_path(base_kernel)

            shutil.copy(
                daemon_path,
                SYSTEM_SERVICES_PATH
            )

            service_daemon_reload(base_kernel)
            service_exec(base_kernel, SERVICE_DAEMON_NAME, 'enable')
            service_exec(base_kernel, SERVICE_DAEMON_NAME, 'start')
        else:
            base_kernel.io.log("Running Webhook listener...")

            # Build command
            command = base_kernel.get_command_resolver(COMMAND_TYPE_ADDON).build_full_command_from_function(
                app__webhook__listen,
                {
                    'port': port
                }
            )

            # Kill old process
            kill_process_by_command(base_kernel, command)

            # Start a new listener
            execute_command(
                base_kernel,
                command.split(),
                async_mode=True
            )

            base_kernel.io.message(f'Started webhook listener on port {port}')

    else:
        class CustomWebhookHttpRequestHandler(WebhookHttpRequestHandler):
            kernel = base_kernel

        if not dry_run:
            with HTTPServer(('', port), CustomWebhookHttpRequestHandler) as server:
                base_kernel.io.log(f'Starting HTTP server on port {port}')
                server.serve_forever()

        base_kernel.io.message(f'Webhook server started on port {port}')
