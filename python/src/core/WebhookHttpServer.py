from http.server import HTTPServer
from src.core.WebhookHttpRequestHandler import WebhookHttpRequestHandler


class WebhookHttpServer:
    path_app_root = False

    def __init__(self, main_entrypoint_path, port):
        class CustomWebhookHttpRequestHandler(WebhookHttpRequestHandler):
            entrypoint_path = main_entrypoint_path

        with HTTPServer(('', port), CustomWebhookHttpRequestHandler) as server:
            server.serve_forever()
