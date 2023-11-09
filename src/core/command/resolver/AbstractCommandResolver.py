import importlib.util
import os
import re
from abc import abstractmethod

from src.core.response.NullResponse import NullResponse
from src.core.response.DictResponse import DictResponse
from src.helper.command import command_to_string
from src.core.response.FunctionResponse import FunctionResponse
from src.core.response.DefaultResponse import DefaultResponse
from src.core.response.AbstractResponse import AbstractResponse
from src.const.globals import COMMAND_SEPARATOR_FUNCTION_PARTS, CORE_COMMAND_NAME, COMMAND_SEPARATOR_ADDON, \
    COMMAND_SEPARATOR_GROUP, VERBOSITY_LEVEL_DEFAULT, COMMAND_EXTENSIONS
from src.helper.args import args_convert_dict_to_args
from src.const.error import ERR_COMMAND_FILE_NOT_FOUND
from src.helper.file import set_owner_for_path_and_ancestors, list_subdirectories
from src.helper.string import trim_leading, to_snake_case, to_kebab_case
from src.helper.system import get_user_or_sudo_user
from src.helper.registry import get_all_commands_from_registry_part
from src.core.CommandRequest import CommandRequest


class AbstractCommandResolver:
    def __init__(self, kernel):
        self.kernel = kernel

    def render_request(self, request: CommandRequest, render_mode: str) -> AbstractResponse | None:
        self.kernel.hook_addons('render_request_pre', {'request': request})

        previous_verbosity = self.kernel.verbosity
        verbosity = request.runner.get_attr('verbosity')

        if verbosity and self.kernel.verbosity == VERBOSITY_LEVEL_DEFAULT:
            self.kernel.verbosity = verbosity

        previous_request = self.kernel.current_request
        self.kernel.current_request = request

        self.kernel.logger.append_request(
            request=request
        )

        # Execute request
        response = self.wrap_response(
            response=request.runner.run()
        )

        # Render response
        response = response.render(
            request=request,
            render_mode=render_mode)

        self.kernel.verbosity = previous_verbosity
        self.kernel.current_request = previous_request

        if response:
            self.kernel.hook_addons(
                'render_request_post',
                {'response': response})

        return response

    def wrap_response(self, response) -> AbstractResponse:
        if isinstance(response, AbstractResponse):
            return response
        elif callable(response):
            return FunctionResponse(self.kernel, response)
        elif isinstance(response, dict):
            return DictResponse(self.kernel, response)
        elif response is None:
            return NullResponse(self.kernel)

        return DefaultResponse(self.kernel, response)

    def get_function(self, command_path: str, parts: list) -> callable:
        # Import module and load function.
        spec = importlib.util.spec_from_file_location(command_path, command_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        return getattr(
            module,
            self.get_function_name(parts)
        )

    @classmethod
    @abstractmethod
    def get_pattern(cls) -> str:
        pass

    def get_commands_registry(self) -> dict:
        if self.get_type() in self.kernel.registry:
            return get_all_commands_from_registry_part(self.kernel.registry[self.get_type()])
        return {}

    @classmethod
    @abstractmethod
    def get_type(cls) -> str:
        pass

    @classmethod
    def build_match(cls, command: str | None):
        return re.match(cls.get_pattern(), command) if command else None

    def get_base_path(self) -> str | None:
        return None

    def get_base_command_path(self) -> str | None:
        base_path = self.get_base_path()

        if not base_path:
            return None

        return os.path.join(base_path, 'command') + '/'

    def set_command_file_permission(self, command_path: str):
        base_path = self.get_base_path()

        if base_path:
            set_owner_for_path_and_ancestors(
                base_path,
                trim_leading(command_path, base_path),
                get_user_or_sudo_user(),
            )

    def create_command_request(self, command: str, args: None | list = None):
        args = args or []

        request = CommandRequest(
            self,
            command,
            args
        )

        return request

    def resolve_alias(self, command: str) -> str:
        registry = self.get_commands_registry()
        for item in registry:
            if command in registry[item]['alias']:
                return item
        return command

    def supports(self, command: str) -> bool:
        command = self.resolve_alias(command)

        if self.build_match(command):
            return True

        return False

    @abstractmethod
    def build_path(self, request: CommandRequest, extension: str, subdir: str = None) -> str | None:
        pass

    def build_path_or_fail(self, request: CommandRequest, extension: str, subdir: str = None):
        path = self.build_path(
            request=request,
            extension=extension,
            subdir=subdir)

        if path is None:
            self.kernel.io.error(ERR_COMMAND_FILE_NOT_FOUND, {
                'command': request.command,
                'path': path,
            })

        return path

    def get_function_name(self, parts: list) -> str | None:
        return to_snake_case(
            COMMAND_SEPARATOR_FUNCTION_PARTS.join(
                self.get_function_name_parts(parts)
            )
        )

    @abstractmethod
    def get_function_name_parts(self, parts: list) -> []:
        pass

    def build_full_command_parts_from_function(self, function_or_command, args: dict = None) -> list:
        if args is None:
            args = []
        else:
            args = args_convert_dict_to_args(function_or_command, args)

        return [
            CORE_COMMAND_NAME,
            self.build_command_from_function(function_or_command),
        ] + args

    def build_full_command_from_function(self, function_or_command, args: dict = None) -> str | None:
        return command_to_string(
            self.build_full_command_parts_from_function(
                function_or_command,
                args
            )
        )

    def build_command_parts_from_function(self, function_name):
        """
        Returns the "default" format (addons style)
        """
        return function_name.split(COMMAND_SEPARATOR_FUNCTION_PARTS)[:3]

    def build_command_parts_from_file_path(self, command_path: str) -> list:
        path_parts = command_path.split(os.sep)

        return [
            path_parts[-4],
            path_parts[-2],
            os.path.splitext(path_parts[-1])[0]
        ]

    def build_command_from_parts(self, parts: list) -> str:
        """
        Returns the "default" format (addons style)
        """
        # Convert each part to kebab-case
        kebab_parts = [to_kebab_case(part) for part in parts]

        return f'{kebab_parts[0]}{COMMAND_SEPARATOR_ADDON}{kebab_parts[1]}{COMMAND_SEPARATOR_GROUP}{kebab_parts[2]}'

    def build_command_from_function(self, function_or_command) -> str | None:
        """
        Returns the "default" format (addons style)
        """
        if isinstance(function_or_command, str):
            return function_or_command

        parts = self.build_command_parts_from_function(function_or_command.callback.__name__)

        return self.build_command_from_parts(parts)

    def build_command_path(self, base_path, extension: str, subdir: str | None, command_path):
        if subdir:
            base_path += f"{subdir}/"

        return os.path.join(base_path, 'command', command_path + '.' + extension)

    def autocomplete_suggest(self, cursor: int, search_split: []) -> str | None:
        return None

    def suggest_arguments(self, command: str, search_params: []):
        request = self.create_command_request(
            command
        )

        # Command is not recognised
        if not request.runner:
            return

        search_params = [val for val in search_params if val.startswith("-")]

        params = []
        for param in request.runner.get_params():
            if any(opt in search_params for opt in param.opts):
                continue

            params += param.opts

        return ' '.join(params)

    def suggest_from_path(self, commands_path: str, search_string: str, test_commands: bool = False) -> []:
        commands = self.scan_commands_groups(commands_path, test_commands)
        commands_names = []

        for command, command_data in commands.items():
            commands_names.append(command)

        # Ignore non relevant values
        commands_names = [
            name for name in commands_names if name.startswith(search_string)
        ]

        return commands_names

    def scan_commands_groups(self, directory: str, test_commands: bool = False):
        command_dict = {}

        if os.path.exists(directory):
            for group in list_subdirectories(directory):
                group_path = os.path.join(directory, group)
                command_dict.update(self.scan_commands(
                    group_path,
                    group,
                    test_commands
                ))

        return command_dict

    def build_alias(self, function, alias: bool | str) -> str:
        if isinstance(alias, bool) and alias:
            return self.build_command_from_function(function)
        return alias

    def scan_commands(self, directory: str, group: str, test_commands: bool = False):
        """Scans the given directory for command files and returns a dictionary of found commands."""
        commands = {}
        for command in os.listdir(directory):
            if command.endswith('.py'):
                command_file = os.path.join(directory, command)
                parts = self.build_command_parts_from_file_path(command_file)

                function = self.get_function(
                    command_file,
                    parts
                )

                if test_commands or not hasattr(function.callback, 'test_command'):
                    test_file = os.path.realpath(os.path.join(directory, '../../tests/command', group, command))

                    commands[self.build_command_from_parts(parts)] = {
                        'file': command_file,
                        'test': test_file if os.path.exists(test_file) else None,
                        'alias': self.get_function_aliases(function)
                    }
        return commands

    def get_function_aliases(self, function) -> list:
        return function.callback.aliases if hasattr(function.callback, 'aliases') else []

    def locate_function(self, request) -> bool:
        # Build dynamic variables
        request.match = self.build_match(request.command)

        if request.match:
            for extension in COMMAND_EXTENSIONS:
                found = request.load_extension(
                    extension
                )

                if found:
                    return True
        return False

    @classmethod
    def decorate_command(cls, function, kwargs):
        return function
