import builtins
import os
import types
from typing import TYPE_CHECKING, Any, Optional, cast

import click

from src.const.types import Args, Kwargs, StringsList, YamlCommand
from src.core.command.resolver.AbstractCommandResolver import AbstractCommandResolver
from src.core.command.runner.AbstractCommandRunner import AbstractCommandRunner
from src.core.command.ScriptCommand import ScriptCommand
from src.core.CommandRequest import CommandRequest
from src.core.response.AbstractResponse import ResponseCollection
from src.core.response.InteractiveShellCommandResponse import (
    InteractiveShellCommandResponse,
)
from src.core.response.QueuedCollectionResponse import QueuedCollectionResponse
from src.decorator.command import command
from src.helper.command import apply_command_decorator
from src.helper.data_yaml import yaml_load
from src.helper.dict import dict_get_item_by_path

if TYPE_CHECKING:
    from src.core.Kernel import Kernel

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

        if request.path:
            self.content = cast(YamlCommand, yaml_load(request.path, {}))

            if not self.content:
                self.kernel.io.error(
                    f"Unable to load yaml script file content :  {request.path}",
                    trace=False,
                )

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
        if not self.request or not self.request.path:
            return None

        content = self.get_content_or_fail()
        scripts = content["scripts"] if "scripts" in content else []
        options = content["options"] if "options" in content else []
        resolver: AbstractCommandResolver = self.request.resolver

        def _script_command_handler(
            *args: Args, **kwargs: Kwargs
        ) -> Optional[QueuedCollectionResponse]:
            commands_collection: ResponseCollection = []

            variables = {}
            for name in kwargs:
                variables[name.upper()] = kwargs[name]

            variables.update(
                {
                    "PATH_CORE": self.kernel.get_path("root"),
                    "PATH_CURRENT": os.getcwd() + os.sep,
                }
            )

            # Iterate through each command in the configuration
            for script in scripts:
                if isinstance(script, str):
                    script = {
                        "script": script,
                        "title": script,
                        "type": COMMAND_TYPE_BASH,
                    }

                self.kernel.io.log(script["title"])

                command = script_command.run_script(
                    script_command.function, self, script, variables
                )

                commands_collection.append(
                    InteractiveShellCommandResponse(self.kernel, command)
                )

            return QueuedCollectionResponse(self.kernel, commands_collection)

        internal_command = resolver.get_function_name(
            resolver.build_command_parts_from_file_path(self.request.path)
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

        if not script_command.function:
            return None

        # Apply extra decorators
        properties = (
            dict_get_item_by_path(data=content, key="properties", default=[]) or []
        )

        for property in properties:
            if isinstance(property, str):
                name = property
                value = None
            else:
                name = list(property.keys())[0]
                value = property[name]

            script_command = apply_command_decorator(
                self.kernel,
                function=script_command,
                group="properties",
                name=name,
                options=value,
            )

        for option in options:
            script_command.function = click.option(
                option["name"],
                option["short"],
                default=option["default"] if "default" in option else False,
                help=option["help"] if "help" in option else None,
                is_flag="is_flag" in option and option["is_flag"],
                required=option["required"] if "required" in option else False,
                type=getattr(builtins, option["type"] if "type" in option else "any"),
            )(script_command.function)

        return cast(ScriptCommand, script_command)

    def run(self) -> Any:
        if not self.request or not self.request.script_command:
            return None

        return self.run_click_function(self.request.script_command)
