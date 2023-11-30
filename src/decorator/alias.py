from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.command.ScriptCommand import ScriptCommand, DecoratedScriptCommand


def alias(name: str) -> "DecoratedScriptCommand":
    def decorator(script_command: "ScriptCommand") -> "ScriptCommand":
        script_command.aliases.append(name)

        return script_command

    return decorator
