from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.command.ScriptCommand import ScriptCommand


def verbosity(level: int):
    def decorator(script_command: "ScriptCommand"):
        # Enforce verbosity level for this function.
        script_command.verbosity = level

        return script_command

    return decorator
