from typing import TYPE_CHECKING

from src.const.types import AnyCallable

if TYPE_CHECKING:
    from src.core.command.ScriptCommand import ScriptCommand


def app_webhook() -> AnyCallable:
    def decorator(script_command: "ScriptCommand") -> "ScriptCommand":
        script_command.set_extra_value("app_webhook")

        return script_command

    return decorator
