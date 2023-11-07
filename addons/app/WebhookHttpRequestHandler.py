from http.server import BaseHTTPRequestHandler

from src.helper.array import array_replace_value
from src.helper.routing import is_allowed_route, get_route_info, get_route_name
from logging.handlers import RotatingFileHandler
import traceback
import logging
import json

WEBHOOK_COMMAND_URL_PLACEHOLDER = '__URL__'


class WebhookHttpRequestHandler(BaseHTTPRequestHandler):
    task_id: str
    log_path: str
    routes: dict

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

            if not is_allowed_route(self.path, self.routes):
                error = 'NOT_FOUND'

            route_name = get_route_name(self.path, self.routes)

            # Create command to execute
            command = array_replace_value(
                self.routes[route_name]['command'],
                WEBHOOK_COMMAND_URL_PLACEHOLDER,
                self.path
            )

            if error:
                self.send_response(500)
                output = {
                    'error': error,
                }
            else:
                self.send_response(200)
                output = {
                    'status': 'started'
                }

            output['task_id'] = self.task_id
            output['command'] = command
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

        # Serialize the output and send the response
        output = json.dumps(output)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(output.encode())
