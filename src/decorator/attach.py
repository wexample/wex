from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict, Union

from src.const.types import StringsList

if TYPE_CHECKING:
    from src.core.command.ScriptCommand import DecoratedScriptCommand, ScriptCommand

CommandAttachmentPassArgsOption = Union[bool, StringsList]


def attach(
    position: str,
    command: str | ScriptCommand,
    pass_args: bool | StringsList = False,
    pass_previous: str | None = None,
) -> DecoratedScriptCommand:
    def decorator(script_command: ScriptCommand) -> ScriptCommand:
        script_command.attachments[position].append(
            {"command": command, "pass_args": pass_args, "pass_previous": pass_previous}
        )

        return script_command

    return decorator


class CommandAttachment(TypedDict, total=False):
    command: str | ScriptCommand
    pass_args: CommandAttachmentPassArgsOption
    pass_previous: str | None
