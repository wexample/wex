from typing import Callable

from addons.app.src.AppCommand import AppCommand
from src.decorator.command import command


def app_command(*decorator_args, **decorator_kwargs) -> Callable[..., AppCommand]:
    def decorator(function) -> "AppCommand":
        # Convert function to command
        return command(*decorator_args, **decorator_kwargs)(function, AppCommand)

    return decorator
