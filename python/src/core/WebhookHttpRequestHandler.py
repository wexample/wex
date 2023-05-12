from http.server import BaseHTTPRequestHandler
from src.core.WebhookHandler import WebhookHandler


class WebhookHttpRequestHandler(BaseHTTPRequestHandler):
    entrypoint_path = False

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        WebhookHandler(self.entrypoint_path).parse_url_and_execute(
            self.path
        )
