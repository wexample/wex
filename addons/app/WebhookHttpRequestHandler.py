from http.server import BaseHTTPRequestHandler
from addons.app.command.webhook.exec import app__webhook__exec
from src.const.globals import KERNEL_RENDER_MODE_HTTP


class WebhookHttpRequestHandler(BaseHTTPRequestHandler):
    kernel = None

    def do_GET(self):

        try:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            response = self.kernel.run_function(
                app__webhook__exec,
                {
                    'url': self.path,
                },
                render_mode=KERNEL_RENDER_MODE_HTTP
            )
            rendered = response.print() or '{"response":null}'

            self.kernel.logger.append_event(
                'EVENT_HTTP_SERVER_RESPONSE',
                {
                    "value": rendered,
                })

            self.wfile.write(rendered.encode())

        except Exception as e:
            import traceback

            message = 'Error during server execution: ' + str(e)

            self.kernel.logger.append_event(
                'EVENT_ERROR_HTTP_SERVER',
                {
                    "error": message,
                    'trace': traceback.format_exc()
                })

            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            empty = '{"error":"Error during server execution: ' + str(e) + '"}'
            self.wfile.write(empty.encode())

            raise
