from typing import TYPE_CHECKING

from src.const.types import AnyCallable

if TYPE_CHECKING:
    from src.core.command.ScriptCommand import ScriptCommand


def alias(name: str) -> AnyCallable:
    def decorator(script_command: "ScriptCommand") -> "ScriptCommand":
        script_command.aliases.append(name)

        return script_command

    return decorator
