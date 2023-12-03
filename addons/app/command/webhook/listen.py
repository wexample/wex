import shutil
import time
from http.server import HTTPServer
from typing import TYPE_CHECKING, Optional

from addons.app.command.webhook.exec import app__webhook__exec
from addons.app.command.webhook.status import app__webhook__status
from addons.app.command.webhook.status_process import app__webhook__status_process
from addons.app.const.webhook import WEBHOOK_LISTENER_ROUTES_MAP
from addons.app.WebhookHttpRequestHandler import (
    WEBHOOK_COMMAND_PATH_PLACEHOLDER,
    WEBHOOK_COMMAND_PORT_PLACEHOLDER,
    WebhookHttpRequestHandler,
)
from addons.system.command.system.is_docker import system__system__is_docker
from src.const.globals import (
    COMMAND_TYPE_ADDON,
    KERNEL_RENDER_MODE_JSON,
    SERVICE_DAEMON_NAME,
    SERVICE_DAEMON_PATH,
    SYSTEM_SERVICES_PATH,
    WEBHOOK_LISTEN_PORT_DEFAULT,
)
from src.const.types import AnyCallable
from src.core.response.AbstractResponse import AbstractResponse
from src.decorator.as_sudo import as_sudo
from src.decorator.command import command
from src.decorator.option import option
from src.helper.command import command_get_option, execute_command_async
from src.helper.core import core_get_daemon_service_resource_path
from src.helper.file import file_remove_file_if_exists
from src.helper.process import process_kill_by_command, process_kill_by_port
from src.helper.system import (
    system_is_port_open,
    system_service_daemon_exec,
    system_service_daemon_reload,
)

if TYPE_CHECKING:
    from src.core.command.ScriptCommand import ScriptCommand
    from src.core.Kernel import Kernel


@as_sudo()
@command(help="Serve webhook listener daemon")
@option(
    "--port",
    "-p",
    type=int,
    required=False,
    default=WEBHOOK_LISTEN_PORT_DEFAULT,
    help="Which port is used by service to listen incoming webhooks",
)
@option(
    "--dry-run",
    "-dr",
    type=bool,
    required=False,
    default=False,
    is_flag=True,
    help="Do not start real service, useful for testing",
)
@option(
    "--asynchronous",
    "-a",
    type=bool,
    required=False,
    default=False,
    is_flag=True,
    help="Use a daemon or not. Can't use daemon in a docker container",
)
@option(
    "--force",
    "-f",
    type=bool,
    required=False,
    default=False,
    is_flag=True,
    help="Kill existing process if already running",
)
def app__webhook__listen(
    kernel: "Kernel",
    port: int = WEBHOOK_LISTEN_PORT_DEFAULT,
    dry_run: bool = False,
    asynchronous: bool = False,
    force: bool = False,
) -> Optional[AbstractResponse]:
    if system_is_port_open(port):
        if force:
            kernel.io.log(f"Port already in use {port}, killing process...")
            process_kill_by_port(port)
            time.sleep(1)
        else:
            kernel.io.error(f"Port already in use {port}", trace=False)
            return None

    # Remove old service file
    file_remove_file_if_exists(SERVICE_DAEMON_PATH)

    if asynchronous:
        use_daemon = not kernel.run_function(system__system__is_docker)

        if use_daemon:
            kernel.logger.append_event(
                "EVENT_WEBHOOK_LISTEN",
                {
                    "launcher": "daemon",
                    "name": SERVICE_DAEMON_NAME,
                },
            )

            daemon_path = core_get_daemon_service_resource_path(kernel)

            shutil.copy(daemon_path, SYSTEM_SERVICES_PATH)

            system_service_daemon_reload(kernel)
            system_service_daemon_exec(kernel, "enable")
            system_service_daemon_exec(kernel, "start")
        else:
            kernel.io.log("Running Webhook listener...")

            # Build command
            command = kernel.get_command_resolver(
                COMMAND_TYPE_ADDON
            ).build_full_command_from_function(app__webhook__listen, {"port": port})

            # Kill old process
            process_kill_by_command(kernel, command)

            # Start a new listener
            process = execute_command_async(
                kernel,
                command.split(),
            )

            kernel.logger.append_event(
                "EVENT_WEBHOOK_LISTEN",
                {
                    "launcher": "async",
                    "command": command,
                },
            )

            kernel.io.message(
                f"Started webhook listener on port {port} in process {process.pid}"
            )
    else:
        try:
            kernel.logger.append_event("EVENT_WEBHOOK_LISTEN", {"launcher": "sync"})

            routes_map = WEBHOOK_LISTENER_ROUTES_MAP.copy()
            for route_name in routes_map:
                script_command: ScriptCommand = routes_map[route_name]["script_command"]
                options = {}
                needs_path = command_get_option(script_command, "webhook_path")
                needs_port_number = command_get_option(
                    script_command, "webhook_port_number"
                )

                if needs_path:
                    options["webhook_path"] = WEBHOOK_COMMAND_PATH_PLACEHOLDER

                if needs_port_number:
                    options["webhook_port_number"] = WEBHOOK_COMMAND_PORT_PLACEHOLDER

                command = kernel.get_command_resolver(
                    COMMAND_TYPE_ADDON
                ).build_full_command_parts_from_script_command(
                    routes_map[route_name]["script_command"],
                    options,
                )

                command += [
                    "--parent-task-id",
                    kernel.get_task_id(),
                    # Allow parsing
                    "--render-mode",
                    KERNEL_RENDER_MODE_JSON,
                    # No need to interact or create sub process
                    "--fast-mode",
                    # Avoid logging to be able to parse output
                    "--quiet",
                ]

                if needs_path:
                    command += [
                        "--webhook-path",
                        WEBHOOK_COMMAND_PATH_PLACEHOLDER,
                    ]

                if needs_port_number:
                    command += [
                        "--webhook-port-number",
                        WEBHOOK_COMMAND_PORT_PLACEHOLDER,
                    ]

                routes_map[route_name]["command"] = command

            # Create a handler with minimal external dependencies.
            class CustomWebhookHttpRequestHandler(WebhookHttpRequestHandler):
                task_id = kernel.get_task_id()
                log_path = kernel.task_file_path("webhook-listener")
                routes = routes_map
                log_stderr: str = kernel.task_file_path("webhook-stderr")
                log_stdout: str = kernel.task_file_path("webhook-stdout")

            if not dry_run:
                with HTTPServer(("", port), CustomWebhookHttpRequestHandler) as server:
                    kernel.io.log(f"Starting HTTP server on port {port}")
                    kernel.logger.append_event("EVENT_WEBHOOK_SERVER_STARTING")
                    server.serve_forever()

            return None

        except Exception as e:
            import traceback

            kernel.logger.append_event(
                "EVENT_ERROR_WEBHOOK_SERVER",
                {
                    "error": "Error during webhook listener execution: " + str(e),
                    "trace": traceback.format_exc(),
                },
            )

            raise

    time.sleep(2)
    return kernel.run_function(app__webhook__status, {"webhook_port_number": port})
