from http.server import BaseHTTPRequestHandler
from src.helper.routing import is_allowed_route, get_route_info
from src.helper.array import array_replace_value
import subprocess
from logging.handlers import RotatingFileHandler
import traceback
import logging
import json
from urllib.parse import urlparse

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
        error = False

        if not is_allowed_route(self.path, self.routes):
            error = 'NOT_FOUND'

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
        output['path'] = self.path
        output['info'] = get_route_info(self.path, self.routes)
        output = json.dumps(output)

        if error:
            self.logger.error(output)
        else:
            self.logger.info(output)

        self.send_header('Content-type', 'application/json')
        self.end_headers()

        self.wfile.write(output.encode())
