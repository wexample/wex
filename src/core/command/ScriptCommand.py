from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional

import click

if TYPE_CHECKING:
    from src.const.types import Args, Kwargs


class ScriptCommand:
    function: Callable
    click_command: click.core.Command

    def __init__(self, function: Callable, command_type: str, decorator_args: 'Args', decorator_kwargs: 'Kwargs') -> None:
        # TODO self.function: Callable = function
        self.command_type: str = command_type

        # TODO RM
        function.command_type = command_type

        from src.const.resolvers import COMMAND_RESOLVERS_CLASSES
        for resolver in COMMAND_RESOLVERS_CLASSES:
            if resolver.get_type() == command_type:
                function = resolver.decorate_command(function)

        # Apply the click.pass_obj decorator
        function = click.pass_obj(function)
        # Apply the original click.command decorator
        click_command: click.core.Command = click.command(*decorator_args, **decorator_kwargs)(function)

        # Add verbosity levels
        click_command = click.option('--fast-mode', '-fast-mode', is_flag=True, required=False,
                                     help="Disable queued scripts execution. Will be faster, but less interactive.")(
            click_command)
        click_command = click.option('--quiet', '-quiet', is_flag=True, required=False,
                                     help="Silent all logs")(click_command)
        click_command = click.option('--vv', '-vv', is_flag=True, required=False,
                                     help="More verbosity")(click_command)
        click_command = click.option('--vvv', '-vvv', is_flag=True, required=False,
                                     help="Maximum verbosity")(click_command)

        # Core commands
        click_command = click.option('--command-request-step', '-command-request-step', type=str, required=False,
                                     help="Core option for processes collection execution")(click_command)
        click_command = click.option('--kernel-task-id', '-kernel-task-id', type=str, required=False,
                                     help="Core option for processes collection execution")(click_command)
        click_command = click.option('--parent-task-id', '-parent-task-id', type=str, required=False,
                                     help="Inform about the parent kernel which have launched current script")(
            click_command)
        click_command = click.option('--log-indent', '-log-indent', type=str, required=False,
                                     help="Core option for processes collection execution")(click_command)
        click_command = click.option('--log-length', '-log-length', type=int, required=False,
                                     help="Change logging frame height, set 0 to disable it")(click_command)
        click_command = click.option('--render-mode', '-render-mode', type=int, required=False,
                                     help="Define render mode (cli, http, ...), which produce different output formatting")(
            click_command)

        self.click_command = click_command
        self.function = click_command  # TODO RM
        self.function.properties = {}

    def run_command(self, runner, function, ctx):
        return self.function.invoke(ctx)

    def run_script(self, function, runner, script: Dict[str, Any], variables: Dict[str, str]) -> Optional[List[str]]:
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

        return script["interpreter"] + [
            script_command] if "interpreter" in script and script_command else script_command
