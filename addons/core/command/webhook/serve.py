import shutil
import click

from addons.system.command.system.is_docker import system__system__is_docker
from src.const.globals import SYSTEM_SERVICES_PATH, SERVICE_DAEMON_NAME, SERVICE_DAEMON_PATH
from src.helper.core import get_daemon_service_resource_path
from src.helper.file import remove_file_if_exists
from src.helper.command import execute_command, build_full_command_from_function
from src.helper.system import is_port_open, kill_process_by_port, kill_process_by_command, service_exec, \
    service_daemon_reload
from src.const.error import ERR_UNEXPECTED
from src.core.WebhookHttpRequestHandler import WebhookHttpRequestHandler
from src.decorator.as_sudo import as_sudo
from http.server import HTTPServer


@click.command()
@click.pass_obj
@as_sudo
@click.option('--port', '-p', type=int, required=False, default=4242)
@click.option('--dry-run', '-dr', type=bool, required=False, default=False, is_flag=True)
@click.option('--asynchronous', '-a', type=bool, required=False, default=False, is_flag=True)
@click.option('--force', '-f', type=bool, required=False, default=False, is_flag=True)
def core__webhook__serve(
        base_kernel,
        port: int = 4242,
        dry_run: bool = False,
        asynchronous: bool = False,
        force: bool = False
):
    if is_port_open(port):
        if force:
            base_kernel.log(f'Port already in use {port}, killing process...')
            kill_process_by_port(port)
        else:
            base_kernel.error(ERR_UNEXPECTED, {
                'error': f'Port already in use {port}',
            })
            return False

    # Remove old service file
    remove_file_if_exists(SERVICE_DAEMON_PATH)

    if asynchronous:
        use_daemon = not base_kernel.exec_function(system__system__is_docker)

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
            base_kernel.log("Running Webhook listener...")

            # Build command
            command = build_full_command_from_function(
                core__webhook__serve,
                {
                    'port': port
                }
            )

            # Kill old process
            kill_process_by_command(base_kernel, command)

            # Start a new listener
            execute_command(
                base_kernel,
                command.split()
            )

            base_kernel.message(f'Started webhook listener on port {port}')

    else:
        class CustomWebhookHttpRequestHandler(WebhookHttpRequestHandler):
            kernel = base_kernel

        if not dry_run:
            with HTTPServer(('', port), CustomWebhookHttpRequestHandler) as server:
                base_kernel.log(f'Starting HTTP server on port {port}')
                server.serve_forever()

        base_kernel.message(f'Webhook server started on port {port}')
