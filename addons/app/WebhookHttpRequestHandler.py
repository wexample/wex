import json
import logging
import subprocess
import traceback
from http.server import BaseHTTPRequestHandler
from logging.handlers import RotatingFileHandler
from typing import Any, Dict, Optional, TypedDict

from addons.app.typing.webhook import WebhookListenerRoutesMap
from src.const.types import Args, Kwargs, StringsList
from src.helper.array import array_replace_value
from src.helper.routing import (
    RouteInfo,
    routing_get_route_info,
    routing_get_route_name,
    routing_is_allowed_route,
)

WEBHOOK_COMMAND_PATH_PLACEHOLDER = "__URL__"
WEBHOOK_COMMAND_PORT_PLACEHOLDER = "__PORT__"
WEBHOOK_STATUS_STARTED = "started"
WEBHOOK_STATUS_STARTING = "starting"
WEBHOOK_STATUS_COMPLETE = "complete"
WEBHOOK_STATUS_ERROR = "error"


class Output(TypedDict, total=False):
    command: StringsList
    details: str
    error: Optional[str]
    info: Optional[RouteInfo]
    path: str
    pid: int
    response: Optional[Dict[Any, Any]]
    status: str
    stderr: str
    task_id: str
    traceback: str


class WebhookHttpRequestHandler(BaseHTTPRequestHandler):
    task_id: str
    log_path: str
    routes: WebhookListenerRoutesMap
    log_stderr: str
    log_stdout: str

    def __init__(self, *args: Args, **kwargs: Kwargs) -> None:
        self.logger = logging.getLogger("wex-webhook")
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(
            RotatingFileHandler(self.log_path, maxBytes=10000, backupCount=5)
        )

        # Request handling is done during init
        super().__init__(*args, **kwargs)

    def do_GET(self) -> None:
        error_code = 500

        try:
            error: Optional[str] = None
            output = Output()

            status = WEBHOOK_STATUS_STARTING
            if not routing_is_allowed_route(self.path, self.routes):
                error = "NOT_FOUND"
                error_code = 404
            else:
                route_name = routing_get_route_name(self.path, self.routes)
                assert isinstance(route_name, str)
                route = self.routes[route_name]

                command = self.routes[route_name]["command"]

                # Create command to execute
                command = array_replace_value(
                    command, WEBHOOK_COMMAND_PATH_PLACEHOLDER, self.path
                )

                command = array_replace_value(
                    command,
                    WEBHOOK_COMMAND_PORT_PLACEHOLDER,
                    str(self.server.server_port),  # type: ignore
                )

                output["command"] = command
                stdout_file = open(self.log_stdout, "w")
                stderr_file = open(self.log_stderr, "w")

                process = subprocess.Popen(
                    command, stdout=stdout_file, stderr=stderr_file, text=True
                )

                if not route["is_async"]:
                    process.communicate()

                    # After the process is complete, you must close the files
                    # before you can read from them.
                    stdout_file.close()
                    stderr_file.close()

                    # Read the output from the files
                    with open(self.log_stdout, "r") as f:
                        stdout = f.read().strip()
                    with open(self.log_stderr, "r") as f:
                        stderr = f.read().strip()

                    try:
                        stdout_dict = json.loads(stdout) if stdout else {}
                    except json.JSONDecodeError:
                        stdout_dict = stdout if stdout else {}

                    if stderr:
                        error = "RESPONSE_ERROR"
                        output["stderr"] = stderr

                    status = WEBHOOK_STATUS_COMPLETE
                    output["response"] = stdout_dict
                else:
                    status = WEBHOOK_STATUS_STARTED

                output["pid"] = process.pid

            if error:
                self.send_response(error_code)
                output["status"] = WEBHOOK_STATUS_ERROR
                output["error"] = error
            else:
                self.send_response(200)
                output["status"] = status

            output["task_id"] = self.task_id
            output["path"] = self.path
            output["info"] = routing_get_route_info(self.path, self.routes)

        except Exception as e:
            # Log the exception with traceback
            self.logger.error("Exception occurred", exc_info=True)
            self.send_response(500)

            output = {
                "error": "WEBHOOK_HANDLER_ERROR",
                "details": str(e),
                "traceback": traceback.format_exc(),
            }

        try:
            # Serialize the output and send the response
            output_str = json.dumps(output)
        except Exception:
            self.logger.error(output)

        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(output_str.encode())
