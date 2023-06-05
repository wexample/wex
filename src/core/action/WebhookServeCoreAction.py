from src.core.action.AbstractCoreAction import AbstractCoreAction
from src.core.WebhookHttpRequestHandler import WebhookHttpRequestHandler
from http.server import HTTPServer


class WebhookServeCoreAction(AbstractCoreAction):
    def exec(self, command, command_args):
        class CustomWebhookHttpRequestHandler(WebhookHttpRequestHandler):
            kernel = self.kernel

        port = 4242
        with HTTPServer(('', port), CustomWebhookHttpRequestHandler) as server:
            self.kernel.log(f'Starting HTTP server on port {port}')
            server.serve_forever()
