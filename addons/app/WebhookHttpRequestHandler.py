from http.server import BaseHTTPRequestHandler
from src.helper.routing import is_allowed_route
from src.helper.array import array_replace_value
import subprocess
from logging.handlers import RotatingFileHandler

import logging

WEBHOOK_COMMAND_URL_PLACEHOLDER = '__URL__'


class WebhookHttpRequestHandler(BaseHTTPRequestHandler):
    log_path: str
    command_base: list

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
            if not is_allowed_route(self.path):
                self.send_error(404, "Not Found")
                return

            # Create command to launch
            command = array_replace_value(
                list(self.command_base),
                WEBHOOK_COMMAND_URL_PLACEHOLDER,
                self.path
            )

            with subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True) as process:
                stdout, stderr = process.communicate()

                if process.returncode != 0:
                    self.logger.error(f"ERROR: {stderr}")
                else:
                    self.logger.info(f"SUCCESS: {stdout}")

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

        except Exception as e:
            import traceback

            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            empty = '{"error":"Error during server execution: ' + str(e) + '"}'
            self.wfile.write(empty.encode())

            raise
