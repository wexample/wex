import shutil

from addons.system.command.system.is_docker import system__system__is_docker
from src.helper.command import execute_command
from src.const.globals import SYSTEM_SERVICES_PATH, SERVICE_DAEMON_NAME, SERVICE_DAEMON_PATH, COMMAND_TYPE_ADDON, \
    WEBHOOK_LISTEN_PORT_DEFAULT, KERNEL_RENDER_MODE_HTTP
from src.helper.core import get_daemon_service_resource_path
from src.helper.file import remove_file_if_exists
from src.helper.system import is_port_open, kill_process_by_port, kill_process_by_command, service_exec, \
    service_daemon_reload
from src.const.error import ERR_UNEXPECTED
from addons.app.WebhookHttpRequestHandler import WebhookHttpRequestHandler, WEBHOOK_COMMAND_URL_PLACEHOLDER
from src.decorator.as_sudo import as_sudo
from http.server import HTTPServer
from src.core.Kernel import Kernel
from src.decorator.command import command
from src.decorator.option import option
from addons.app.command.webhook.exec import app__webhook__exec


@command(help="Serve webhook listener daemon")
@as_sudo()
@option('--port', '-p', type=int, required=False, default=WEBHOOK_LISTEN_PORT_DEFAULT,
        help="Which port is used by service to listen incoming webhooks")
@option('--dry-run', '-dr', type=bool, required=False, default=False, is_flag=True,
        help="Do not start real service, useful for testing")
@option('--asynchronous', '-a', type=bool, required=False, default=False, is_flag=True,
        help="Use a daemon or not. Can't use daemon in a docker container")
@option('--force', '-f', type=bool, required=False, default=False, is_flag=True,
        help="Kill existing process if already running")
def app__webhook__listen(
        kernel: Kernel,
        port: int = WEBHOOK_LISTEN_PORT_DEFAULT,
        dry_run: bool = False,
        asynchronous: bool = False,
        force: bool = False
):
    if is_port_open(port):
        if force:
            kernel.io.log(f'Port already in use {port}, killing process...')
            kill_process_by_port(port)
        else:
            kernel.io.error(ERR_UNEXPECTED, {
                'error': f'Port already in use {port}',
            })
            return False

    # Remove old service file
    remove_file_if_exists(SERVICE_DAEMON_PATH)

    if asynchronous:
        use_daemon = not kernel.run_function(system__system__is_docker)

        if use_daemon:
            kernel.logger.append_event('EVENT_WEBHOOK_LISTEN', {
                "launcher": "daemon",
                "name": SERVICE_DAEMON_NAME,
            })

            daemon_path = get_daemon_service_resource_path(kernel)

            shutil.copy(
                daemon_path,
                SYSTEM_SERVICES_PATH
            )

            service_daemon_reload(kernel)
            service_exec(kernel, SERVICE_DAEMON_NAME, 'enable')
            service_exec(kernel, SERVICE_DAEMON_NAME, 'start')
        else:
            kernel.io.log("Running Webhook listener...")

            # Build command
            command = kernel.get_command_resolver(COMMAND_TYPE_ADDON).build_full_command_from_function(
                app__webhook__listen,
                {
                    'port': port
                }
            )

            # Kill old process
            kill_process_by_command(kernel, command)

            # Start a new listener
            process = execute_command(
                kernel,
                command.split(),
                async_mode=True
            )

            kernel.logger.append_event('EVENT_WEBHOOK_LISTEN', {
                "launcher": "async",
                "command": command,
            })

            kernel.io.message(f'Started webhook listener on port {port}')

            return process

    else:
        try:
            kernel.logger.append_event('EVENT_WEBHOOK_LISTEN', {
                "launcher": "sync"
            })

            # prepare base command to launch.
            command = kernel.get_command_resolver(
                COMMAND_TYPE_ADDON).build_full_command_parts_from_function(
                app__webhook__exec,
                {
                    'render-mode': KERNEL_RENDER_MODE_HTTP,
                    'url': WEBHOOK_COMMAND_URL_PLACEHOLDER,
                },
            )

            command += [
                '--parent-task-id',
                kernel.task_id,
                # No need to interact or create sub process
                '--fast-mode'
            ]

            # Create a handler with minimal external dependencies.
            class CustomWebhookHttpRequestHandler(WebhookHttpRequestHandler):
                log_path = kernel.task_file_path('webhook-listener')
                command_base = command

            if not dry_run:
                with HTTPServer(('', port), CustomWebhookHttpRequestHandler) as server:
                    kernel.io.log(f'Starting HTTP server on port {port}')
                    kernel.logger.append_event('EVENT_WEBHOOK_SERVER_STARTING')
                    server.serve_forever()

            kernel.io.message(f'Webhook server started on port {port}')

        except Exception as e:
            import traceback

            kernel.logger.append_event('EVENT_ERROR_WEBHOOK_SERVER', {
                "error": 'Error during webhook listener execution: ' + str(e),
                'trace': traceback.format_exc()
            })

            raise
