from typing import TYPE_CHECKING

from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.helper.docker import docker_build_long_container_name
from src.const.globals import SHELL_DEFAULT
from src.const.types import (
    AnyCallable,
    Args,
    CoreCommandArgsDict,
    Kwargs,
    StringsList,
    YamlCommandScript,
)
from src.core.command.ScriptCommand import ScriptCommand
from src.helper.command import command_escape
from src.helper.string import string_replace_multiple

if TYPE_CHECKING:
    from src.core.command.runner.AbstractCommandRunner import AbstractCommandRunner


class AppCommand(ScriptCommand):
    def __init__(
        self,
        function: AnyCallable,
        command_type: str,
        decorator_args: "Args",
        decorator_kwargs: "Kwargs",
    ) -> None:
        # Get and pop interesting args
        dir_required = decorator_kwargs.pop("dir_required", True)
        should_run = decorator_kwargs.pop("should_run", False)

        super().__init__(
            function,
            command_type,
            decorator_args,
            decorator_kwargs,
        )

        # Do not provide app_dir to function
        self.set_extra_value("app_dir_required", dir_required)

        self.click_command = app_dir_option(required=dir_required)(self.click_command)

        # Do not check if app is running
        self.set_extra_value("app_should_run", should_run)

    def run_script(
        self,
        runner: "AbstractCommandRunner",
        script: YamlCommandScript,
        variables: CoreCommandArgsDict,
    ) -> StringsList:
        from addons.app.AppAddonManager import AppAddonManager

        kernel = runner.kernel
        manager = kernel.addons["app"]
        assert isinstance(manager, AppAddonManager)

        if manager.app_dir:
            import os

            from dotenv import dotenv_values

            from addons.app.const.app import APP_FILEPATH_REL_DOCKER_ENV

            env_path = os.path.join(manager.app_dir, APP_FILEPATH_REL_DOCKER_ENV)

            app_variables = dotenv_values(env_path)
            if "script" in script and isinstance(script["script"], str):
                script["script"] = string_replace_multiple(
                    script["script"], app_variables
                )
            elif "file" in script and isinstance(script["file"], str):
                script["file"] = string_replace_multiple(script["file"], app_variables)

            command = super().run_script(runner, script, variables)

            if "container_name" in script and isinstance(script["container_name"], str):
                from src.helper.command import command_to_string

                command_string = command_to_string(command)
                command_string = command_escape(command_string)

                wrap_command = [
                    "docker",
                    "exec",
                    docker_build_long_container_name(kernel, script["container_name"]),
                    SHELL_DEFAULT,
                    "-c",
                    command_string,
                ]

                return wrap_command
        else:
            command = super().run_script(runner, script, variables)

        return command
