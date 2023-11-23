from src.core.FunctionProperty import FunctionProperty
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.command.ScriptCommand import ScriptCommand


def app_webhook(*args, **kwargs):
    def decorator(script_command: 'ScriptCommand'):
        FunctionProperty(
            script_command,
            'app_webhook',
            True)

        return script_command

    return decorator
