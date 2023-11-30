import click

from src.const.types import AnyCallable


def service_option() -> AnyCallable:
    def decorator(function: AnyCallable) -> AnyCallable:
        # Add the --app-dir option
        function = click.option(
            "--service", "-s", type=str, required=True, help="Service name"
        )(function)

        return function

    return decorator
