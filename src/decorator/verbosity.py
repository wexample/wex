from typing import TYPE_CHECKING

from src.const.types import AnyCallable

if TYPE_CHECKING:
    from src.core.command.ScriptCommand import ScriptCommand


def verbosity(level: int) -> AnyCallable:
    def decorator(script_command: "ScriptCommand") -> "ScriptCommand":
        # Enforce verbosity level for this function.
        script_command.verbosity = level

        return script_command

    return decorator
