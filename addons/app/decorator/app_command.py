from __future__ import annotations

from typing import TYPE_CHECKING

from src.const.types import AnyCallable, Args, Kwargs

if TYPE_CHECKING:
    from addons.app.src.AppCommand import AppCommand


def app_command(*decorator_args: Args, **decorator_kwargs: Kwargs) -> AnyCallable:
    def decorator(function: AnyCallable) -> AppCommand:
        from addons.app.src.AppCommand import AppCommand
        from src.decorator.command import command

        # Convert function to command
        app_script_command = command(*decorator_args, **decorator_kwargs)(
            function, AppCommand
        )
        assert isinstance(app_script_command, AppCommand)

        return app_script_command

    return decorator
