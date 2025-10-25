from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, cast

from src.const.types import AnyCallable, Args, Kwargs

if TYPE_CHECKING:
    from src.core.command.TestCommand import TestCommand


def test_command(*args: Args, **kwargs: Kwargs) -> Callable[..., TestCommand]:
    if "help" not in kwargs:
        kwargs["help"] = "A test command"

    def decorator(function: AnyCallable) -> TestCommand:
        from src.core.command.TestCommand import TestCommand
        from src.decorator.command import command

        return cast(TestCommand, command(*args, **kwargs)(function, TestCommand))

    return decorator
