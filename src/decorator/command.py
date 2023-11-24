from src.core.command.ScriptCommand import ScriptCommand
from src.const.globals import COMMAND_TYPE_ADDON
from typing import Callable


# Define your custom decorator
def command(*decorator_args, **decorator_kwargs) -> Callable[..., ScriptCommand]:
    if 'help' not in decorator_kwargs:
        raise ValueError("The 'help' argument is required for the custom command decorator.")

    def decorator(f: Callable, script_command_class=ScriptCommand) -> ScriptCommand:
        return script_command_class(
            f,
            decorator_kwargs.pop('command_type', COMMAND_TYPE_ADDON),
            decorator_args,
            decorator_kwargs)

    return decorator
