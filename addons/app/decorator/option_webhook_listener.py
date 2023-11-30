import click

from src.const.types import AnyCallable
from src.const.globals import WEBHOOK_LISTEN_PORT_DEFAULT


def option_webhook_listener(port_number: bool = False, path: bool = False) -> AnyCallable:
    def decorator(function: AnyCallable) -> AnyCallable:
        if port_number:
            function = click.option(
                "--webhook-port-number",
                "-wpn",
                type=int,
                help="Webhook listener port number",
                required=True,
                default=WEBHOOK_LISTEN_PORT_DEFAULT,
            )(function)

        if path:
            function = click.option(
                "--webhook-path",
                "-wp",
                type=str,
                help="Webhook requested path",
                required=True,
            )(function)

        return function

    return decorator
