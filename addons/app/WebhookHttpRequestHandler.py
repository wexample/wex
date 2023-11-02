from http import HTTPStatus
from http.server import BaseHTTPRequestHandler
from addons.app.command.webhook.exec import app__webhook__exec
from src.const.globals import KERNEL_RENDER_MODE_HTTP


class WebhookHttpRequestHandler(BaseHTTPRequestHandler):
    kernel = None

    def do_GET(self):
        self.send_header('Content-type', 'application/json')

        try:
            self.send_response(200)
            self.end_headers()

            success = self.kernel.run_function(
                app__webhook__exec,
                {
                    'url': self.path,
                },
                render_mode=KERNEL_RENDER_MODE_HTTP
            ).first()

            if success:
                self.wfile.write(success.encode())
            else:
                self.wfile.write(b'{"error":"empty"}')

        except Exception as e:
            import traceback

            self.kernel.logger.append_event({
                "error": 'Error during server execution: ' + str(e),
                'trace': traceback.format_exc()
            })

            self.send_response(500)
            self.end_headers()
            self.wfile.write(b'{"error":"Error during server execution: ' + str(e) + '"}')

            raise
