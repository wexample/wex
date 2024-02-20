from typing import TYPE_CHECKING, TypedDict, Union

from src.const.types import StringsList

if TYPE_CHECKING:
    from src.core.command.ScriptCommand import DecoratedScriptCommand, ScriptCommand

CommandAttachmentPassArgsOption = Union[bool, StringsList]


class CommandAttachment(TypedDict):
    command: Union[str, "ScriptCommand"]
    pass_args: CommandAttachmentPassArgsOption


def attach(
    position: str,
    command: Union[str, "ScriptCommand"],
    pass_args: Union[bool, StringsList] = False,
) -> "DecoratedScriptCommand":
    def decorator(script_command: "ScriptCommand") -> "ScriptCommand":
        script_command.attachments[position].append(
            {
                "command": command,
                "pass_args": pass_args
            }
        )

        return script_command

    return decorator
