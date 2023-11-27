from typing import Callable

import click


def service_option() -> Callable[[Callable], Callable]:
    def decorator(f):
        if callable(f):
            # Add the --app-dir option
            f = click.option(
                "--service", "-s", type=str, required=True, help="Service name"
            )(f)

        return f

    return decorator
