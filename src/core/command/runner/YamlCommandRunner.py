import builtins
import os
import types
from typing import TYPE_CHECKING, Any, Optional, cast

import click
from wexample_helpers_yaml.helpers.yaml_helpers import yaml_read
from wexample_wex_core.helpers.click_helper import click_args_convert_dict_to_args

from src.const.types import (
    Args,
    CoreCommandArgsDict,
    Kwargs,
    StringsList,
    YamlCommand,
    YamlCommandScript,
)
from src.core.CommandRequest import CommandRequest
from src.core.command.ScriptCommand import ScriptCommand
from src.core.command.resolver.AbstractCommandResolver import AbstractCommandResolver
from src.core.command.runner.AbstractCommandRunner import AbstractCommandRunner
from src.core.response.AbstractResponse import AbstractResponse, ResponseCollection
from src.core.response.InteractiveShellCommandResponse import (
    InteractiveShellCommandResponse,
)
from src.core.response.ResponseCollectionResponse import ResponseCollectionResponse
from src.decorator.command import command
from src.helper.command import apply_command_decorator, internal_command_to_shell
from wexample_helpers.helpers.dict_helper import dict_get_item_by_path

if TYPE_CHECKING:
    from src.utils.kernel import Kernel

COMMAND_TYPE_BASH: str = "bash"
COMMAND_TYPE_BASH_FILE: str = "bash-file"
COMMAND_TYPE_PYTHON: str = "python"
COMMAND_TYPE_PYTHON_FILE: str = "python-file"


class YamlCommandRunner(AbstractCommandRunner):
    def __init__(self, kernel: "Kernel") -> None:
        super().__init__(kernel)
        self.content: Optional[YamlCommand] = None

    def set_request(self, request: CommandRequest) -> None:
        super().set_request(request=request)
        path = request.get_path()

        if path:
            self.content = self.load_yaml_command(path)

            if not self.content:
                self.kernel.io.error(
                    f"Unable to load yaml script file content : {path}",
                    trace=False,
                )

    def load_yaml_command(self, path: str) -> YamlCommand:
        return cast(YamlCommand, yaml_read(path, {}))

    def get_options_names(self) -> StringsList:
        names = []
        content = self.get_content_or_fail()

        if "options" in content:
            options = content["options"]

            for option in options:
                names.append(option["name"])
                names.append(option["short"])

        return names

    def get_content_or_fail(self) -> YamlCommand:
        if not self.content:
            self.kernel.io.error(
                "Trying to access request content before initialization"
            )
            assert False

        return self.content

    def get_command_type(self) -> str:
        return self.get_content_or_fail()["type"]

    def build_script_command(self) -> Optional[ScriptCommand]:
        request = self.get_request()
        content = self.get_content_or_fail()

        scripts = content["scripts"] if "scripts" in content else []
        options = content["options"] if "options" in content else []
        resolver: AbstractCommandResolver = request.resolver

        def _script_command_handler(
            *args: Args, **kwargs: Kwargs
        ) -> Optional[ResponseCollectionResponse]:
            commands_collection: ResponseCollection = []

            variables: CoreCommandArgsDict = {}
            assert isinstance(variables, dict)

            for name in kwargs:
                variables[name.upper()] = kwargs[name]

            variables.update(
                {
                    "PATH_CORE": self.kernel.directory.path,
                    "PATH_CURRENT": os.getcwd() + os.sep,
                }
            )

            # Iterate through each command in the configuration
            for script in scripts:
                script_config: YamlCommandScript

                if isinstance(script, str):
                    script_config = cast(
                        YamlCommandScript,
                        {
                            "script": script,
                            "title": script,
                            "type": COMMAND_TYPE_BASH,
                        },
                    )
                else:
                    script_config = script

                if not "title" in script_config:
                    if "script" in script_config:
                        script_config["title"] = script_config["script"]
                    elif "command" in script_config:
                        script_config["title"] = script_config["command"]

                self.kernel.io.log(script_config["title"])

                if "command" in script_config:
                    command_str = str(script_config["command"])
                    command_request: CommandRequest = (
                        self.kernel.create_command_request(command_str)
                    )

                    command_list = internal_command_to_shell(
                        kernel=self.kernel,
                        internal_command=command_str,
                        args=click_args_convert_dict_to_args(
                            command_request.get_script_command().click_command,
                            cast(
                                CoreCommandArgsDict,
                                script_config["options"]
                                if "options" in script_config
                                else {},
                            ),
                        ),
                    )
                else:
                    command_list = script_command.run_script(
                        self, script_config, variables
                    )

                storage_variable = None
                if "variable" in script_config:
                    storage_variable = script_config["variable"]

                response: AbstractResponse

                response = InteractiveShellCommandResponse(
                    self.kernel, command_list, as_sudo_user=False
                )

                if storage_variable:
                    variables[storage_variable] = response

                commands_collection.append(response)

            return ResponseCollectionResponse(self.kernel, commands_collection)

        internal_command = resolver.get_function_name(
            resolver.build_command_parts_from_file_path(self.get_request().get_path())
        )

        # Function must have the appropriate name,
        # allowing to guess internal command name from it
        click_function_callback = types.FunctionType(
            _script_command_handler.__code__,
            _script_command_handler.__globals__,
            internal_command,
            _script_command_handler.__defaults__,
            _script_command_handler.__closure__,
        )

        decorator_name = dict_get_item_by_path(content, "command.decorator")
        if decorator_name:
            decorator = self.kernel.decorators["command"][decorator_name]
        else:
            decorator = command

        if "help" not in content:
            self.kernel.io.error(
                f"Missing help section in command {internal_command}", trace=False
            )

        decorator_options = dict_get_item_by_path(content, "command.options", {})
        script_command = decorator(help=content["help"], **decorator_options)(
            click_function_callback
        )

        if not script_command.click_command:
            return None

        # Apply extra decorators
        properties = (
            dict_get_item_by_path(data=content, key="properties", default=[]) or []
        )

        for property in properties:
            if isinstance(property, str):
                name = property
                property_options = None
            else:
                name = property["name"]
                property_options = property["options"]

            script_command = apply_command_decorator(
                self.kernel,
                function=script_command,
                group="properties",
                name=name,
                options=property_options,
            )

        for option in options:
            script_command.click_command = click.option(
                option["name"],
                option["short"],
                default=option["default"] if "default" in option else False,
                help=option["help"] if "help" in option else None,
                is_flag="is_flag" in option and option["is_flag"],
                required=option["required"] if "required" in option else False,
                type=getattr(builtins, option["type"] if "type" in option else "any"),
            )(script_command.click_command)

        return cast(ScriptCommand, script_command)

    def run(self) -> Any:
        return self.run_click_function(self.get_request().get_script_command())
