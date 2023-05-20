from http.server import BaseHTTPRequestHandler
from src.core.WebhookHandler import WebhookHandler


class WebhookHttpRequestHandler(BaseHTTPRequestHandler):
    entrypoint_path = False

    def do_GET(self):
        try:
            success = WebhookHandler(self.entrypoint_path).parse_url_and_execute(
                self.path,
                {
                    'ip': self.client_address[0],
                    'port': self.client_address[1],
                    'method': self.command,
                    'user_agent': self.headers.get('User-Agent')
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
