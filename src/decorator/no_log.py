from typing import TYPE_CHECKING

from src.const.types import AnyCallable

if TYPE_CHECKING:
    from src.core.command.ScriptCommand import ScriptCommand


def no_log() -> AnyCallable:
    def decorator(script_command: "ScriptCommand") -> "ScriptCommand":
        # Say that the function execution is not stored in log file,
        # Used for log command itself or autocomplete suggestion.
        script_command.no_log = True

        return script_command

    return decorator
