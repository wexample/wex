import click

from src.const.types import AnyCallable, Args, Kwargs


def app_dir_option(*args: Args, **kwargs: Kwargs) -> AnyCallable:
    def decorator(function: click.core.Command) -> click.core.Command:
        # Add the --app-dir option
        return click.option(
            "--app-dir", "-a", type=str, help="App directory", **kwargs
        )(function)

    return decorator
