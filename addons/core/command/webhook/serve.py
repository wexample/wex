import os
import signal
import subprocess
import click

from src.helper.command import execute_command, build_full_command_from_function
from src.helper.system import is_port_open, kill_process_by_port
from src.const.error import ERR_UNEXPECTED
from src.core.WebhookHttpRequestHandler import WebhookHttpRequestHandler
from src.decorator.as_sudo import as_sudo
from http.server import HTTPServer


@click.command()
@click.pass_obj
@as_sudo
@click.option('--port', '-p', type=int, required=False, default=4242)
@click.option('--dry-run', '-dr', type=bool, required=False, default=False, is_flag=True)
@click.option('--asynchronous', '-a', type=bool, required=False, default=False, is_flag=True)
@click.option('--force', '-f', type=bool, required=False, default=False, is_flag=True)
def core__webhook__serve(
        base_kernel,
        port: int = 4242,
        dry_run: bool = False,
        asynchronous: bool = False,
        force: bool = False
):

    if is_port_open(port):
        if force:
            base_kernel.log(f'Port already in use {port}, killing process...')
            kill_process_by_port(port)
        else:
            base_kernel.error(ERR_UNEXPECTED, {
                'error': f'Port already in use {port}',
            })
            return False

    if asynchronous:
        base_kernel.log("Running Webhook listener...")

        command = build_full_command_from_function(
            core__webhook__serve,
            {
                'port': port
            }
        )

        process = execute_command(
            base_kernel,
            [
                'pgrep',
                '-f',
                command
            ],
            # Sync mode.
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        out, err = process.communicate()

        for pid in out.splitlines():
            os.kill(int(pid), signal.SIGTERM)

        # Start a new listener
        execute_command(
            base_kernel,
            command.split()
        )

        base_kernel.message(f'Started webhook listener on port {port}')

    else:
        class CustomWebhookHttpRequestHandler(WebhookHttpRequestHandler):
            kernel = base_kernel

        if not dry_run:
            with HTTPServer(('', port), CustomWebhookHttpRequestHandler) as server:
                base_kernel.log(f'Starting HTTP server on port {port}')
                server.serve_forever()

        base_kernel.message(f'Webhook server started on port {port}')
