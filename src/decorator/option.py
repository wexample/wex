from typing import TYPE_CHECKING

import click

if TYPE_CHECKING:
    from src.const.types import DecoratedCallable


# Define your custom decorator
def option(*args, **kwargs) -> 'DecoratedCallable':
    def decorator(f):
        if callable(f):
            # Apply the original click.option decorator
            f = click.option(*args, **kwargs)(f)
        return f

    return decorator
