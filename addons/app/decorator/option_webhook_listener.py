import click

from src.const.types import AnyCallable
from src.const.globals import WEBHOOK_LISTEN_PORT_DEFAULT


def option_webhook_listener(port=False, path=False) -> AnyCallable:
    def decorator(function: AnyCallable) -> AnyCallable:
        if port:
            function.option_webhook_listener_port = True

            function = click.option(
                "--port",
                "-p",
                type=int,
                help="Webhook listener port number",
                required=True,
                default=WEBHOOK_LISTEN_PORT_DEFAULT,
            )(function)

        if path:
            function.option_webhook_listener_path = True

            function = click.option(
                "--path",
                "-p",
                type=str,
                help="Webhook requested path",
                required=True,
            )(function)

        return function

    return decorator
