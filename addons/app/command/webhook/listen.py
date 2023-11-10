import shutil

from addons.system.command.system.is_docker import system__system__is_docker
from addons.app.command.webhook.status import app__webhook__status
from addons.app.command.webhook.status_process import app__webhook__status_process
from src.helper.command import execute_command
from src.const.globals import SYSTEM_SERVICES_PATH, SERVICE_DAEMON_NAME, SERVICE_DAEMON_PATH, COMMAND_TYPE_ADDON, \
    WEBHOOK_LISTEN_PORT_DEFAULT, KERNEL_RENDER_MODE_JSON
from src.helper.core import get_daemon_service_resource_path
from src.helper.file import remove_file_if_exists
from src.helper.system import is_port_open, kill_process_by_port, kill_process_by_command, service_exec, \
    service_daemon_reload
from addons.app.WebhookHttpRequestHandler import WebhookHttpRequestHandler, WEBHOOK_COMMAND_PATH_PLACEHOLDER, \
    WEBHOOK_COMMAND_PORT_PLACEHOLDER
from src.decorator.as_sudo import as_sudo
from http.server import HTTPServer
from src.core.Kernel import Kernel
from src.decorator.command import command
from src.decorator.option import option
from addons.app.command.webhook.exec import app__webhook__exec

WEBHOOK_LISTENER_ROUTES_MAP = {
    'exec': {
        'async': True,
        'pattern': r'^/webhook/([a-zA-Z0-9_\-]+)/([a-zA-Z0-9_\-]+)$',
        'function': app__webhook__exec
    },
    'status': {
        'async': False,
        'pattern': r'^/status$',
        'function': app__webhook__status,
    },
    'status_process': {
        'async': False,
        'pattern': r'^/status/process/([0-9\-]+)$',
        'function': app__webhook__status_process
    },
}


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
            import time
            time.sleep(1)
        else:
            kernel.io.error(f'Port already in use {port}', trace=False)
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

            routes_map = WEBHOOK_LISTENER_ROUTES_MAP.copy()
            for route_name in routes_map:
                function = routes_map[route_name]['function']
                options = {}

                if hasattr(function.callback, 'option_webhook_listener_path'):
                    options['path'] = WEBHOOK_COMMAND_PATH_PLACEHOLDER

                if hasattr(function.callback, 'option_webhook_listener_port'):
                    options['port'] = WEBHOOK_COMMAND_PORT_PLACEHOLDER

                command = kernel.get_command_resolver(
                    COMMAND_TYPE_ADDON).build_full_command_parts_from_function(
                    routes_map[route_name]['function'],
                    options,
                )

                command += [
                    '--parent-task-id',
                    kernel.task_id,
                    # Allow parsing
                    '--render-mode',
                    KERNEL_RENDER_MODE_JSON,
                    # No need to interact or create sub process
                    '--fast-mode',
                    # Avoid logging to be able to parse output
                    '--quiet'
                ]

                if kernel.root_request.function_has_attr(name='option_webhook_listener_path'):
                    command += [
                        '--path',
                        WEBHOOK_COMMAND_PATH_PLACEHOLDER,
                    ]

                if kernel.root_request.function_has_attr(name='option_webhook_listener_port'):
                    command += [
                        '--port',
                        WEBHOOK_COMMAND_PORT_PLACEHOLDER,
                    ]

                routes_map[route_name]['command'] = command

            # Create a handler with minimal external dependencies.
            class CustomWebhookHttpRequestHandler(WebhookHttpRequestHandler):
                task_id = kernel.task_id
                log_path = kernel.task_file_path('webhook-listener')
                routes = routes_map
                log_stderr: str = kernel.task_file_path('webhook-stderr')
                log_stdout: str = kernel.task_file_path('webhook-stdout')

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
