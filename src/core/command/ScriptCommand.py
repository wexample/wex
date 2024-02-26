from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, cast

import click

from src.const.types import (
    AnyCallable,
    Args,
    CoreCommandArgsDict,
    Kwargs,
    StringKeysDict,
    StringsList,
    YamlCommandScript,
)
from src.core.BaseClass import BaseClass
from src.decorator.attach import CommandAttachment

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager
    from src.core.command.runner.AbstractCommandRunner import AbstractCommandRunner


class ScriptCommand(BaseClass):
    def __init__(
        self,
        function: AnyCallable,
        command_type: str,
        decorator_args: "Args",
        decorator_kwargs: "Kwargs",
    ) -> None:
        self.ai_tool: bool = False
        self.aliases: StringsList = []
        self.as_sudo: bool = False
        self.command_type: str = command_type
        self.no_log: bool = False
        self.attachments: Dict[str, List[CommandAttachment]] = {
            "after": [],
            "before": [],
        }
        self.verbosity: Optional[int] = None
        self._extra: StringKeysDict = {}

        from src.const.resolvers import COMMAND_RESOLVERS_CLASSES

        for resolver in COMMAND_RESOLVERS_CLASSES:
            if resolver.get_type() == command_type:
                function = resolver.decorate_command(function)

        # Apply the click.pass_obj decorator
        function = click.pass_obj(function)
        # Apply the original click.command decorator
        click_command: click.core.Command = click.command(
            *decorator_args, **decorator_kwargs
        )(function)

        # Add verbosity levels
        click_command = click.option(
            "--fast-mode",
            "-fast-mode",
            is_flag=True,
            required=False,
            help="Disable queued scripts execution. Will be faster, but less interactive.",
        )(click_command)
        click_command = click.option(
            "--quiet", "-quiet", is_flag=True, required=False, help="Silent all logs"
        )(click_command)
        click_command = click.option(
            "--vv", "-vv", is_flag=True, required=False, help="More verbosity"
        )(click_command)
        click_command = click.option(
            "--vvv", "-vvv", is_flag=True, required=False, help="Maximum verbosity"
        )(click_command)

        # Core commands
        click_command = click.option(
            "--command-request-step",
            "-command-request-step",
            type=str,
            required=False,
            help="Core option for processes collection execution",
        )(click_command)
        click_command = click.option(
            "--kernel-task-id",
            "-kernel-task-id",
            type=str,
            required=False,
            help="Core option for processes collection execution",
        )(click_command)
        click_command = click.option(
            "--parent-task-id",
            "-parent-task-id",
            type=str,
            required=False,
            help="Inform about the parent kernel which have launched current script",
        )(click_command)
        click_command = click.option(
            "--log-indent",
            "-log-indent",
            type=str,
            required=False,
            help="Core option for processes collection execution",
        )(click_command)
        click_command = click.option(
            "--log-length",
            "-log-length",
            type=int,
            required=False,
            help="Change logging frame height, set 0 to disable it",
        )(click_command)
        click_command = click.option(
            "--render-mode",
            "-render-mode",
            type=int,
            required=False,
            help="Define render mode (cli, http, ...), which produce different output formatting",
        )(click_command)

        self.click_command: click.core.Command = click_command

    def set_extra_value(self, name: str, value: bool = True) -> None:
        self._extra[name] = value

    def get_extra_value(self, name: str, default: Optional[Any] = None) -> Any:
        return self._extra[name] if name in self._extra else default

    def get_extra_properties(self) -> StringKeysDict:
        return self._extra

    def run_command(
        self, runner: "AbstractCommandRunner", ctx: click.core.Context
    ) -> Any:
        return self.click_command.invoke(ctx)

    def run_script(
        self,
        runner: "AbstractCommandRunner",
        script: YamlCommandScript,
        variables: CoreCommandArgsDict,
    ) -> StringsList:
        from src.helper.string import string_replace_multiple

        if "script" in script:
            from src.helper.command import command_escape

            script_string: str = str(script["script"])
            script_string = string_replace_multiple(script_string, variables)

            if "interpreter" in script:
                script_string = command_escape(script_string)
        elif "file" in script:
            script_string = string_replace_multiple(script["file"], variables)

            manager: "AppAddonManager" = cast(
                "AppAddonManager", runner.kernel.addons["app"]
            )

            script["interpreter"] = script.get(
                "interpreter", [manager.get_service_shell()]
            )
        else:
            runner.kernel.io.error(
                'Missing "script" or "file" key in script yaml definition', trace=False
            )
            assert False

        return (
            script["interpreter"] + [script_string]
            if "interpreter" in script and script_string
            else [script_string]
        )

    def get_callback(self) -> AnyCallable:
        self._validate__should_not_be_none(self.click_command.callback)
        assert self.click_command.callback is not None

        return self.click_command.callback

    def get_callback_name(self) -> str:
        return self.get_callback().__name__


DecoratedScriptCommand = Callable[..., ScriptCommand]
