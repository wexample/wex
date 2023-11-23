from src.core.FunctionProperty import FunctionProperty

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.command.ScriptCommand import ScriptCommand


def no_log():
    def decorator(script_command: 'ScriptCommand'):
        # Say that the function execution is not stored in log file,
        # Used for log command itself or autocomplete suggestion.
        FunctionProperty(
            script_command,
            'no_log',
            True)

        return script_command

    return decorator
