import click

from src.const.globals import COMMAND_TYPE_ADDON
from typing import List, Optional, Dict, Any


# Define your custom decorator
def command(*args, **kwargs):
    if 'help' not in kwargs:
        raise ValueError("The 'help' argument is required for the custom command decorator.")

    def decorator(f):
        if callable(f):
            f.command_type = kwargs.pop('command_type', COMMAND_TYPE_ADDON)

            if f.command_type:
                from src.const.resolvers import COMMAND_RESOLVERS_CLASSES
                for resolver in COMMAND_RESOLVERS_CLASSES:
                    if resolver.get_type() == f.command_type:
                        f = resolver.decorate_command(f, kwargs)

            # Apply the click.pass_obj decorator
            f = click.pass_obj(f)
            # Apply the original click.command decorator
            f = click.command(*args, **kwargs)(f)

            # Add verbosity levels
            f = click.option('--fast-mode', '-fast-mode', is_flag=True, required=False,
                             help="Disable queued scripts execution. Will be faster, but less interactive.")(f)
            f = click.option('--quiet', '-quiet', is_flag=True, required=False,
                             help="Silent all logs")(f)
            f = click.option('--vv', '-vv', is_flag=True, required=False,
                             help="More verbosity")(f)
            f = click.option('--vvv', '-vvv', is_flag=True, required=False,
                             help="Maximum verbosity")(f)

            # Core commands
            f = click.option('--command-request-step', '-command-request-step', type=str, required=False,
                             help="Core option for processes collection execution")(f)
            f = click.option('--kernel-task-id', '-kernel-task-id', type=str, required=False,
                             help="Core option for processes collection execution")(f)
            f = click.option('--parent-task-id', '-parent-task-id', type=str, required=False,
                             help="Inform about the parent kernel which have launched current script")(f)
            f = click.option('--log-indent', '-log-indent', type=str, required=False,
                             help="Core option for processes collection execution")(f)
            f = click.option('--log-length', '-log-length', type=int, required=False,
                             help="Change logging frame height, set 0 to disable it")(f)
            f = click.option('--render-mode', '-render-mode', type=int, required=False,
                             help="Define render mode (cli, http, ...), which produce different output formatting")(f)

            f.run_handler = _command_run
            f.script_run_handler = _script_run
            f.properties = {}
        return f

    return decorator


def _command_run(runner, function, ctx):
    return function.invoke(ctx)


def _script_run(function, runner, script: Dict[str, Any], env_args: Dict[str, str]) -> Optional[List[str]]:
    from src.helper.string import replace_variables

    if "script" in script:
        script_command = replace_variables(script["script"], env_args)
    elif "file" in script:
        script_command = replace_variables(script["file"], env_args)
        script["interpreter"] = script.get("interpreter", ["/bin/bash"])
    else:
        script_command = None

    return script["interpreter"] + [script_command] if "interpreter" in script and script_command else script_command
