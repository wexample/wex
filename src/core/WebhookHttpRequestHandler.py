from http.server import BaseHTTPRequestHandler
from addons.core.command.webhook.exec import core__webhook__exec


class WebhookHttpRequestHandler(BaseHTTPRequestHandler):
    kernel = None

    def do_GET(self):
        try:
            success = self.kernel.exec_function(
                core__webhook__exec,
                {
                    'url': self.path,
                }
            )

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            if success:
                self.wfile.write(b'RUNNING')
            else:
                self.wfile.write(b'ERROR')

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write("ERROR : {}".format(e).encode())
