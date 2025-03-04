import os
import re
from abc import abstractmethod
from typing import Any, Dict, List, Optional, cast

from wexample_helpers.helpers.string import string_to_snake_case, string_to_kebab_case
from wexample_helpers.helpers.file import file_list_subdirectories
from wexample_wex_core.helpers.click_helper import click_args_convert_dict_to_args

from src.const.globals import (
    COMMAND_EXTENSIONS,
    COMMAND_SEPARATOR_ADDON,
    COMMAND_SEPARATOR_FUNCTION_PARTS,
    COMMAND_SEPARATOR_GROUP,
    CORE_COMMAND_NAME,
    VERBOSITY_LEVEL_DEFAULT,
)
from src.const.types import (
    AnyCallable,
    OptionalCoreCommandArgsDict,
    OptionalCoreCommandArgsListOrDict,
    RegistryCommand,
    RegistryCommandsCollection,
    RegistryResolverData,
    ShellCommandsList,
    StringKeysDict,
    StringsList,
    StringsMatch,
)
from src.core.CommandRequest import CommandRequest
from src.utils.abstract_kernel_child import AbsractKernelChild
from src.core.command.ScriptCommand import ScriptCommand
from src.core.response.AbortResponse import AbortResponse
from src.core.response.AbstractResponse import AbstractResponse
from src.core.response.DefaultResponse import DefaultResponse
from src.core.response.DictResponse import DictResponse
from src.core.response.FunctionResponse import FunctionResponse
from src.core.response.ListResponse import ListResponse
from src.core.response.NullResponse import NullResponse
from src.decorator.attach import CommandAttachment
from src.helper.command import command_to_string
from src.helper.file import (
    file_set_owner_for_path_and_ancestors,
)
from src.helper.string import (
    string_trim_leading,
)
from src.helper.user import get_user_or_sudo_user


class AbstractCommandResolver(AbsractKernelChild):
    def render_request(
        self, request: CommandRequest, render_mode: str
    ) -> "AbstractResponse":
        runner = request.get_runner()

        self.kernel.hook_addons("render_request_pre", {"request": request})
        self.execute_all_attached(request, "before")

        previous_verbosity = self.kernel.verbosity
        script_command = request.get_script_command()

        if (
            script_command.verbosity is not None
            and self.kernel.verbosity == VERBOSITY_LEVEL_DEFAULT
        ):
            self.kernel.verbosity = script_command.verbosity

        previous_request = self.kernel.current_request
        self.kernel.current_request = request

        self.kernel.logger.log_request(request=request)

        # Execute request
        response = self.wrap_response(response=runner.run())

        # Render response
        response.render(request=request, render_mode=render_mode)

        self.kernel.verbosity = previous_verbosity
        self.kernel.current_request = previous_request

        if response:
            self.kernel.hook_addons("render_request_post", {"response": response})

            # Ensure this is the real end of command, no repetition planned.
            if not response.has_next_step:
                self.execute_all_attached(request, "after", previous=response)

        return response

    def execute_attached(
        self,
        request: "CommandRequest",
        position: str,
        previous: Optional[AbstractResponse] = None,
    ) -> None:
        request_command_string = request.get_string_command()
        commands = self.get_active_commands()
        for command_string in commands:
            if len(commands[command_string]["attachments"][position]):
                for attachment_config in commands[command_string]["attachments"][
                    position
                ]:
                    attachment = cast(CommandAttachment, attachment_config)

                    if attachment["command"] == request_command_string:
                        self.kernel.io.log(
                            f"Running attached command to {request_command_string} : {command_string}"
                        )

                        args: StringKeysDict = {}
                        args_copy: StringKeysDict = cast(
                            StringKeysDict, request.get_args_dict().copy()
                        )

                        # Pass all args, attached command should have same args as target
                        if attachment["pass_previous"] and previous:
                            args[attachment["pass_previous"]] = previous.print_wrapped()

                        if attachment["pass_args"] is True:
                            args = args_copy
                        # Pass some args
                        elif isinstance(attachment["pass_args"], list):
                            for arg_name in attachment["pass_args"]:
                                # Support missing args as arg can have a default value.
                                if arg_name in args_copy:
                                    args[arg_name] = args_copy[arg_name]

                        response = self.kernel.run_command(
                            command_string,
                            args,
                            # Attached script runs in fast mode as it can contain async responses:
                            #   - On "before": it should be executed completely
                            #   - On "after": it should avoid to run main command with extra unexpected steps.
                            fast_mode=True,
                        )

                        self.kernel.io.log(response.print_wrapped())

    def get_active_commands(self) -> RegistryCommandsCollection:
        return self.get_commands_registry()

    def execute_all_attached(
        self,
        request: "CommandRequest",
        position: str,
        previous: Optional[AbstractResponse] = None,
    ) -> None:
        # Ask every other resolver to call each attached command type
        for resolver in self.kernel.resolvers:
            self.kernel.resolvers[resolver].execute_attached(
                request, position, previous=previous
            )

    def wrap_response(self, response: Any) -> "AbstractResponse":
        if isinstance(response, AbstractResponse):
            return response
        elif callable(response):
            return FunctionResponse(self.kernel, response)
        elif isinstance(response, dict):
            return DictResponse(self.kernel, response)
        elif isinstance(response, list):
            return ListResponse(self.kernel, response)
        elif response is None:
            return NullResponse(self.kernel)

        return DefaultResponse(self.kernel, response)

    @classmethod
    @abstractmethod
    def get_pattern(cls) -> str:
        pass

    def get_commands_registry(self) -> RegistryCommandsCollection:
        from src.helper.registry import registry_get_all_commands_from_registry_part

        if self.get_type() in self.kernel.registry_structure.content.resolvers:
            return registry_get_all_commands_from_registry_part(
                self.get_registry_data()
            )

        return {}

    @classmethod
    @abstractmethod
    def get_type(cls) -> str:
        pass

    @classmethod
    def build_match(cls, command: str) -> Optional[StringsMatch]:
        import re
        return re.match(cls.get_pattern(), command) if command else None

    def get_base_path(self) -> Optional[str]:
        return None

    def get_base_command_path(self) -> str | None:
        base_path = self.get_base_path()

        if not base_path:
            return None

        return self.build_base_command_path(base_path)

    def build_base_command_path(self, base_path: str) -> str:
        return os.path.join(base_path, "command") + os.path.sep

    def set_command_file_permission(self, command_path: str) -> None:
        base_path = self.get_base_path()

        if base_path:
            file_set_owner_for_path_and_ancestors(
                base_path,
                string_trim_leading(command_path, base_path),
                get_user_or_sudo_user(),
            )

    def create_command_request(
        self, command: str, args: Optional["OptionalCoreCommandArgsListOrDict"] = None
    ) -> CommandRequest:
        return CommandRequest(self, command, args or [])

    def resolve_alias(self, command: str) -> str:
        registry = self.get_commands_registry()
        for item in registry:
            if command in registry[item]["alias"]:
                return item
        return command

    def supports(self, command: str) -> bool:
        command = self.resolve_alias(command)

        if self.build_match(command):
            return True

        return False

    @abstractmethod
    def build_path(
        self, request: CommandRequest, extension: str, subdir: Optional[str] = None
    ) -> Optional[str]:
        pass

    def build_path_or_fail(
        self, request: CommandRequest, extension: str, subdir: Optional[str] = None
    ) -> str:
        path = self.build_path(request=request, extension=extension, subdir=subdir)

        if path is None:
            self.kernel.io.error(
                "Command file not found for command {command}",
                {
                    "command": request.get_string_command(),
                },
                trace=False,
            )

        assert path is not None

        return path

    def get_function_name(self, parts: List[str]) -> str:
        return string_to_snake_case(
            COMMAND_SEPARATOR_FUNCTION_PARTS.join(self.get_function_name_parts(parts))
        )

    @abstractmethod
    def get_function_name_parts(self, parts: StringsList) -> StringsList:
        pass

    def build_full_command_parts_from_script_command(
        self,
        script_command: ScriptCommand,
        args: Optional["OptionalCoreCommandArgsDict"] = None,
    ) -> "ShellCommandsList":
        return [
            CORE_COMMAND_NAME,
            self.build_command_from_function(script_command),
        ] + (
            click_args_convert_dict_to_args(script_command.click_command, args)
            if args
            else []
        )

    def build_full_command_from_function(
        self, script_command: ScriptCommand, args: OptionalCoreCommandArgsDict = None
    ) -> str:
        return command_to_string(
            self.build_full_command_parts_from_script_command(script_command, args)
        )

    def build_command_parts_from_function_name(
        self, function_name: str
    ) -> "ShellCommandsList":
        """
        Returns the "default" format (addons style)
        """
        return function_name.split(COMMAND_SEPARATOR_FUNCTION_PARTS)[:3]

    def build_command_parts_from_file_path(self, command_path: str) -> StringsList:
        path_parts = command_path.split(os.sep)

        return [path_parts[-4], path_parts[-2], os.path.splitext(path_parts[-1])[0]]

    def build_command_from_parts(self, parts: StringsList) -> str:
        """
        Returns the "default" format (addons style)
        """
        # Convert each part to kebab-case
        kebab_parts = [string_to_kebab_case(part) for part in parts]

        return f"{kebab_parts[0]}{COMMAND_SEPARATOR_ADDON}{kebab_parts[1]}{COMMAND_SEPARATOR_GROUP}{kebab_parts[2]}"

    def build_command_from_function(self, script_command: ScriptCommand) -> str:
        if (
            not script_command.click_command
            or not script_command.click_command.callback
        ):
            self.kernel.io.error(
                "Trying to build command name from non-located command function"
            )

        parts = self.build_command_parts_from_function_name(
            script_command.click_command.callback.__name__
        )

        return self.build_command_from_parts(parts)

    def build_command_path(
        self, base_path: str, extension: str, subdir: Optional[str], command_path: str
    ) -> str:
        if subdir:
            base_path += f"{subdir}/"

        return os.path.join(base_path, "command", command_path + "." + extension)

    def autocomplete_suggest(
        self, cursor: int, search_split: StringsList
    ) -> str | None:
        return None

    def suggest_arguments(self, command: str, search: str) -> str:
        request = self.create_command_request(command)

        # Command is not recognised
        if not request._runner:
            return ""

        function_params = request.get_runner().get_options_names()
        search_params = [param for param in function_params if param.startswith(search)]

        return " ".join(search_params)

    def suggest_from_path(
        self, commands_path: str, search_string: str, test_commands: bool = False
    ) -> StringsList:
        commands = self.scan_commands_groups(commands_path, test_commands)
        commands_names: StringsList = []

        for command, command_data in commands.items():
            commands_names.append(command)

        # Ignore non relevant values
        commands_names = [
            name for name in commands_names if name.startswith(search_string)
        ]

        return commands_names

    def scan_commands_groups(
        self, directory: str, test_commands: bool = False
    ) -> RegistryCommandsCollection:
        command_dict: RegistryCommandsCollection = {}

        if os.path.exists(directory):
            for group in file_list_subdirectories(directory):
                group_path = os.path.join(directory, group)
                command_dict.update(
                    self.scan_commands(group_path, group, test_commands)
                )

        return command_dict

    def scan_commands(
        self, directory: str, group: str, test_commands: bool = False
    ) -> RegistryCommandsCollection:
        """Scans the given directory for command files and returns a dictionary of found commands."""
        commands: RegistryCommandsCollection = {}

        for command_file_name in os.listdir(directory):
            extension = command_file_name.rsplit(".", 1)[-1]
            if extension in COMMAND_EXTENSIONS:
                command_file = os.path.join(directory, command_file_name)
                parts = self.build_command_parts_from_file_path(command_file)
                internal_command = self.build_command_from_parts(parts)
                request = self.create_command_request(internal_command)

                if request._runner:
                    script_command = request.get_runner().build_script_command()

                    if script_command:
                        test_file = None
                        if test_commands or not hasattr(
                            script_command.click_command.callback, "test_command"
                        ):
                            # All test are in python
                            test_file = os.path.realpath(
                                os.path.join(
                                    directory,
                                    "../../tests/command",
                                    group,
                                    command_file_name.rsplit(".", 1)[0] + ".py",
                                )
                            )

                            test_file = (
                                test_file
                                if (test_file and os.path.exists(test_file))
                                else None
                            )

                        attachments: Dict[str, List[CommandAttachment]] = {}
                        for position in script_command.attachments:
                            attachments_list: List[CommandAttachment] = []
                            for attachment in script_command.attachments[position]:
                                if isinstance(attachment["command"], ScriptCommand):
                                    attachment_string = (
                                        self.build_command_from_function(
                                            attachment["command"]
                                        )
                                    )
                                else:
                                    assert isinstance(attachment["command"], str)
                                    attachment_string = attachment["command"]

                                attachments_list.append(
                                    {
                                        "command": attachment_string,
                                        "pass_args": attachment["pass_args"],
                                        "pass_previous": attachment["pass_previous"],
                                    }
                                )

                            attachments[position] = attachments_list

                        commands[internal_command] = cast(
                            RegistryCommand,
                            {
                                "alias": self.get_script_command_aliases(
                                    script_command
                                ),
                                "attachments": attachments,
                                "command": internal_command,
                                "description": script_command.click_command.help,
                                "file": command_file,
                                "properties": script_command.get_extra_properties(),
                                "test": test_file,
                            },
                        )
        return commands

    def get_script_command_aliases(self, script_command: ScriptCommand) -> List[str]:
        return script_command.aliases

    def locate_function(self, request: CommandRequest) -> bool:
        # Build dynamic variables
        request.match = self.build_match(request.get_string_command())

        if request.match:
            for extension in COMMAND_EXTENSIONS:
                found = request.load_extension(extension)

                if found:
                    return True
        return False

    @classmethod
    def decorate_command(cls, function: "AnyCallable") -> "AnyCallable":
        return function

    def run_command_request_from_url_path(
        self, path: str, args: OptionalCoreCommandArgsDict = None
    ) -> "AbstractResponse":
        command = self.create_command_from_path(path)

        if not command:
            return AbortResponse(self.kernel, "COMMAND_NOT_FOUND_FROM_PATH")

        return self.kernel.run_command(
            command=command, args=cast(OptionalCoreCommandArgsListOrDict, args)
        )

    def create_command_from_path(self, path: str) -> Optional[str]:
        parts = path.split(os.sep)

        if not parts:
            return None

        command_parts = self.build_command_parts_from_url_path_parts(parts)

        if not command_parts:
            return None

        return self.build_command_from_parts(command_parts)

    @abstractmethod
    def build_command_parts_from_url_path_parts(
        self, path_parts: StringsList
    ) -> StringsList:
        pass

    def build_registry_data(self, test: bool = False) -> "RegistryResolverData":
        return {}

    def get_registry_data(self) -> "RegistryResolverData":
        return self.kernel.registry_structure.get_resolver_data(self.get_type())
