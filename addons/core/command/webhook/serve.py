import click
from src.core.WebhookHttpRequestHandler import WebhookHttpRequestHandler
from http.server import HTTPServer


@click.command()
@click.pass_obj
@click.option('--port', '-p', type=int, required=False, default=4242)
@click.option('--dry-run', '-dr', type=bool, required=False, default=False, is_flag=True)
def core__webhook__serve(base_kernel, port: int = 4242, dry_run: bool = False):
    class CustomWebhookHttpRequestHandler(WebhookHttpRequestHandler):
        kernel = base_kernel

    if not dry_run:
        with HTTPServer(('', port), CustomWebhookHttpRequestHandler) as server:
            base_kernel.log(f'Starting HTTP server on port {port}')
            server.serve_forever()
