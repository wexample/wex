from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from src.core.command.ScriptCommand import DecoratedScriptCommand, ScriptCommand


def attach(position: str, command: Union[str, "ScriptCommand"]) -> "DecoratedScriptCommand":
    def decorator(script_command: "ScriptCommand") -> "ScriptCommand":
        script_command.attachments[position].append(command)

        return script_command

    return decorator
