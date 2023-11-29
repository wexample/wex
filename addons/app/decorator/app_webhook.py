from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.command.ScriptCommand import ScriptCommand


def app_webhook(*args, **kwargs):
    def decorator(script_command: "ScriptCommand"):
        script_command.set_extra_value('app_webhook')

        return script_command

    return decorator
