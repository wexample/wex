from src.core.command.ScriptCommand import ScriptCommand
from src.const.globals import COMMAND_TYPE_ADDON
from typing import List, Optional, Dict, Any
from typing import Callable


# Define your custom decorator
def command(*args, **kwargs) -> Callable[..., ScriptCommand]:
    if 'help' not in kwargs:
        raise ValueError("The 'help' argument is required for the custom command decorator.")

    def decorator(f: Callable, script_command_class=ScriptCommand) -> ScriptCommand:
        # f.run_handler = _command_run
        # f.script_run_handler = _script_run

        command = script_command_class(
            f,
            kwargs.pop('command_type', COMMAND_TYPE_ADDON),
            args,
            kwargs)

        # TODO RM
        command.function.run_handler = _command_run
        command.function.script_run_handler = _script_run

        return command

    return decorator


def _command_run(runner, function, ctx):
    return function.invoke(ctx)


def _script_run(function, runner, script: Dict[str, Any], variables: Dict[str, str]) -> Optional[List[str]]:
    from src.helper.string import string_replace_multiple

    if 'script' in script:
        from src.helper.command import command_escape
        script_command = string_replace_multiple(script['script'], variables)

        if 'interpreter' in script:
            script_command = command_escape(script_command)

    elif 'file' in script:
        script_command = string_replace_multiple(script['file'], variables)
        script["interpreter"] = script.get("interpreter", ["/bin/bash"])
    else:
        script_command = None

    return script["interpreter"] + [script_command] if "interpreter" in script and script_command else script_command
