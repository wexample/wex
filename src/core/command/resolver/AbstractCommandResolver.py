import os
import re
from abc import abstractmethod
from typing import Any, List, Optional, cast

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
    CoreCommandStringParts,
    OptionalCoreCommandArgsDict,
    OptionalCoreCommandArgsListOrDict,
    RegistryCommand,
    RegistryCommandsCollection,
    RegistryResolverData,
    StringsList,
)
from src.core.command.runner.AbstractCommandRunner import AbstractCommandRunner
from src.core.command.ScriptCommand import ScriptCommand
from src.core.CommandRequest import CommandRequest
from src.core.KernelChild import KernelChild
from src.core.response.AbortResponse import AbortResponse
from src.core.response.AbstractResponse import AbstractResponse
from src.core.response.DefaultResponse import DefaultResponse
from src.core.response.DictResponse import DictResponse
from src.core.response.FunctionResponse import FunctionResponse
from src.core.response.NullResponse import NullResponse
from src.helper.args import args_convert_dict_to_args
from src.helper.command import command_to_string
from src.helper.file import (
    file_list_subdirectories,
    file_set_owner_for_path_and_ancestors,
)
from src.helper.string import (
    string_to_kebab_case,
    string_to_snake_case,
    string_trim_leading,
)
from src.helper.user import get_user_or_sudo_user


class AbstractCommandResolver(KernelChild):
    def render_request(
        self, request: CommandRequest, render_mode: str
    ) -> "AbstractResponse":
        runner = cast(AbstractCommandRunner, request.runner)

        self.kernel.hook_addons("render_request_pre", {"request": request})

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

        return response

    def wrap_response(self, response: Any) -> "AbstractResponse":
        if isinstance(response, AbstractResponse):
            return response
        elif callable(response):
            return FunctionResponse(self.kernel, response)
        elif isinstance(response, dict):
            return DictResponse(self.kernel, response)
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
    def build_match(cls, command: str) -> Optional[re.Match[str]]:
        return re.match(cls.get_pattern(), command) if command else None

    def get_base_path(self) -> Optional[str]:
        return None

    def get_base_command_path(self) -> str | None:
        base_path = self.get_base_path()

        if not base_path:
            return None

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
                'Command file not found for command {command}, in path "{path}"',
                {
                    "command": request.get_string_command(),
                    "path": path,
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
    ) -> "CoreCommandStringParts":
        return [
            CORE_COMMAND_NAME,
            self.build_command_from_function(script_command),
        ] + (
            args_convert_dict_to_args(script_command.click_command, args)
            if args
            else []
        )

    def build_full_command_from_function(
        self, script_command: ScriptCommand, args: OptionalCoreCommandArgsDict = None
    ) -> str | None:
        return command_to_string(
            self.build_full_command_parts_from_script_command(script_command, args)
        )

    def build_command_parts_from_function_name(
        self, function_name: str
    ) -> "CoreCommandStringParts":
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

    def suggest_arguments(self, command: str, search_params: str) -> str:
        request = self.create_command_request(command)

        # Command is not recognised
        if not request.runner:
            return ""

        function_params = request.runner.get_options_names()
        search_params = [
            param for param in function_params if param.startswith(search_params)
        ]

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

                if request.runner:
                    script_command = request.runner.build_script_command()

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

                        commands[internal_command] = cast(
                            RegistryCommand,
                            {
                                "command": internal_command,
                                "file": command_file,
                                "test": test_file,
                                "alias": self.get_script_command_aliases(
                                    script_command
                                ),
                                "properties": script_command.get_extra_properties(),
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

    def run_command_request_from_url_path(self, path: str) -> "AbstractResponse":
        command = self.create_command_from_path(path)

        if not command:
            return AbortResponse(self.kernel, "COMMAND_NOT_FOUND_FROM_PATH")

        return self.kernel.run_command(command=command, args={})

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
