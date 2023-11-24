from typing import Callable, cast, Any

from src.core.command.TestCommand import TestCommand
from src.decorator.command import command
from src.const.types import AnyCallable, Args, Kwargs


def test_command(*args: Args, **kwargs: Kwargs) -> Callable[..., Any]:
    if 'help' not in kwargs:
        kwargs['help'] = 'A test command'

    def decorator(function: AnyCallable) -> TestCommand:
        return cast(
            TestCommand,
            command(*args, **kwargs)(function, TestCommand))

    return decorator
