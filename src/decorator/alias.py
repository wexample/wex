from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.command.ScriptCommand import ScriptCommand


def alias(name: bool | str = True):
    def decorator(script_command: "ScriptCommand"):
        script_command.aliases.append(name)

        return script_command

    return decorator
