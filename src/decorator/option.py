import click

from src.const.types import AnyCallable, Args, Kwargs


# Define your custom decorator
def option(*args: Args, **kwargs: Kwargs) -> AnyCallable:
    def decorator(function: AnyCallable) -> AnyCallable:
        # Apply the original click.option decorator
        return click.option(*args, **kwargs)(function)

    return decorator
