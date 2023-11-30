from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.command.ScriptCommand import ScriptCommand, DecoratedScriptCommand


def no_log() -> "DecoratedScriptCommand":
    def decorator(script_command: "ScriptCommand") -> "ScriptCommand":
        # Say that the function execution is not stored in log file,
        # Used for log command itself or autocomplete suggestion.
        script_command.no_log = True

        return script_command

    return decorator
