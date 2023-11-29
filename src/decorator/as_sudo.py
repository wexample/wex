from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.command.ScriptCommand import ScriptCommand


def as_sudo():
    def decorator(script_command: "ScriptCommand"):
        # Say that the function is not allowed to be executed without sudo permissions.
        script_command.as_sudo = True

        return script_command

    return decorator
