from http.server import BaseHTTPRequestHandler
from src.helper.routing import is_allowed_route
from src.helper.array import array_replace_value
import subprocess
from logging.handlers import RotatingFileHandler
import traceback
import logging
import json

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

            # Create command to execute
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

            stdout = stdout.strip()
            error = False

            # Check if the process returned an error
            if process.returncode != 0:
                error = 'UNEXPECTED_ERROR'
            if stdout:
                # Attempt to parse the stdout as JSON to verify valid JSON response
                try:
                    json.loads(stdout)  # If this fails, an exception will be raised
                except json.JSONDecodeError:
                    error = 'INVALID_RESPONSE'
            else:
                error = 'EMPTY_RESPONSE'

            if error:
                self.send_response(500)
                stdout = json.dumps({
                    'error': error,
                    'stdout': command
                })
                self.logger.error(stdout)
            else:
                self.send_response(200)

            self.send_header('Content-type', 'application/json')
            self.end_headers()

            # If stdout is valid JSON, log the info
            self.logger.info(f"{stdout}")
            self.wfile.write(stdout.encode())

        except Exception as e:
            traceback_string = traceback.format_exc()  # Get detailed traceback
            self.logger.error(f'Exception during processing: {traceback_string}')

            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            error_response = f'{{"error":"Error during server execution: {str(e)}"}}'
            self.wfile.write(error_response.encode())
            # Raise the exception for further handling if needed
            raise
