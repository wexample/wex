import subprocess
from http.server import BaseHTTPRequestHandler

from src.helper.array import array_replace_value
from src.helper.routing import is_allowed_route, get_route_info, get_route_name
from logging.handlers import RotatingFileHandler
import traceback
import logging
import json

WEBHOOK_COMMAND_URL_PLACEHOLDER = '__URL__'
WEBHOOK_STATUS_STARTED = 'started'
WEBHOOK_STATUS_STARTING = 'starting'
WEBHOOK_STATUS_COMPLETE = 'complete'
WEBHOOK_STATUS_ERROR = 'error'


class WebhookHttpRequestHandler(BaseHTTPRequestHandler):
    task_id: str
    log_path: str
    routes: dict
    log_stderr: str
    log_stdout: str

    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger('wex-webhook')
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(
            RotatingFileHandler(
                self.log_path,
                maxBytes=10000,
                backupCount=5
            )
        )

        # Request handling is done during init
        super().__init__(*args, **kwargs)

    def do_GET(self):
        try:
            error = False
            output = {}

            status = WEBHOOK_STATUS_STARTING
            if not is_allowed_route(self.path, self.routes):
                error = 'NOT_FOUND'
            else:
                route_name = get_route_name(self.path, self.routes)
                route = self.routes[route_name]

                # Create command to execute
                command = array_replace_value(
                    self.routes[route_name]['command'],
                    WEBHOOK_COMMAND_URL_PLACEHOLDER,
                    self.path
                )

                output['command'] = command
                stdout_file = open(self.log_stdout, 'w')
                stderr_file = open(self.log_stderr, 'w')

                process = subprocess.Popen(
                    command,
                    stdout=stdout_file,
                    stderr=stderr_file,
                    text=True)

                if not route['async']:
                    stdout, stderr = process.communicate()
                    stdout = stdout.strip() if isinstance(stdout, str) else stdout
                    stderr = stderr.strip() if isinstance(stderr, str) else stderr

                    try:
                        stdout = json.loads(stdout) if stdout else {}
                    except json.JSONDecodeError:
                        stdout = stdout if stdout else {}

                    if stderr:
                        error = 'RESPONSE_ERROR'

                    status = WEBHOOK_STATUS_COMPLETE
                    output['response'] = stdout
                else:
                    status = WEBHOOK_STATUS_STARTED

                output['pid'] = process.pid

            if error:
                self.send_response(500)
                output['status'] = WEBHOOK_STATUS_ERROR
                output['error'] = error
            else:
                self.send_response(200)
                output['status'] = status

            output['task_id'] = self.task_id
            output['path'] = self.path
            output['info'] = get_route_info(self.path, self.routes)

        except Exception as e:
            # Log the exception with traceback
            self.logger.error("Exception occurred", exc_info=True)
            self.send_response(500)

            output = {
                'error': 'WEBHOOK_HANDLER_ERROR',
                'details': str(e),
                'traceback': traceback.format_exc()
            }

        try:
            # Serialize the output and send the response
            output = json.dumps(output)
        except Exception as e:
            self.logger.error(output)

        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(output.encode())
