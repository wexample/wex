from src.const.globals import COMMAND_TYPE_ADDON
from src.const.types import AnyCallable, Args, Kwargs
from src.core.command.ScriptCommand import DecoratedScriptCommand, ScriptCommand


# Define your custom decorator
def command(
    *decorator_args: Args, **decorator_kwargs: Kwargs
) -> "DecoratedScriptCommand":
    if "help" not in decorator_kwargs:
        raise ValueError(
            "The 'help' argument is required for the custom command decorator."
        )

    def decorator(
        f: AnyCallable, script_command_class: type = ScriptCommand
    ) -> ScriptCommand:
        script_command = script_command_class(
            f,
            decorator_kwargs.pop("command_type", COMMAND_TYPE_ADDON),
            decorator_args,
            decorator_kwargs,
        )

        assert isinstance(script_command, ScriptCommand)

        return script_command

    return decorator
