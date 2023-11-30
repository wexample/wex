from typing import Callable, cast

from src.const.types import AnyCallable, Args, Kwargs
from src.core.command.TestCommand import TestCommand
from src.decorator.command import command


def test_command(*args: Args, **kwargs: Kwargs) -> Callable[..., TestCommand]:
    if "help" not in kwargs:
        kwargs["help"] = "A test command"

    def decorator(function: AnyCallable) -> TestCommand:
        return cast(TestCommand, command(*args, **kwargs)(function, TestCommand))

    return decorator
