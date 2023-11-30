from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.command.ScriptCommand import DecoratedScriptCommand, ScriptCommand


def verbosity(level: int) -> "DecoratedScriptCommand":
    def decorator(script_command: "ScriptCommand") -> "ScriptCommand":
        # Enforce verbosity level for this function.
        script_command.verbosity = level

        return script_command

    return decorator
