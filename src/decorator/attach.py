from typing import TYPE_CHECKING, TypedDict, Union

from src.const.types import StringsList

if TYPE_CHECKING:
    from src.core.command.ScriptCommand import DecoratedScriptCommand, ScriptCommand

CommandAttachmentPassArgsOption = Union[bool, StringsList]


class CommandAttachment(TypedDict):
    command: Union[str, "ScriptCommand"]
    pass_args: CommandAttachmentPassArgsOption
    pass_previous: bool


def attach(
    position: str,
    command: Union[str, "ScriptCommand"],
    pass_args: Union[bool, StringsList] = False,
    pass_previous: bool = False,
) -> "DecoratedScriptCommand":
    def decorator(script_command: "ScriptCommand") -> "ScriptCommand":
        script_command.attachments[position].append(
            {
                "command": command,
                "pass_args": pass_args,
                "pass_previous": pass_previous
            }
        )

        return script_command

    return decorator
