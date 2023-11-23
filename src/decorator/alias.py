from src.core.FunctionProperty import FunctionProperty
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.command.ScriptCommand import ScriptCommand


def alias(name: bool | str = True):
    def decorator(script_command: 'ScriptCommand'):
        aliases = FunctionProperty.get_property(script_command, 'aliases')
        if aliases:
            aliases.append(name)
        else:
            FunctionProperty(
                script_command,
                'aliases',
                [name])

        return script_command

    return decorator
