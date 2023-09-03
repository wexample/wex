import importlib.util
import os
import re
import sys
from abc import abstractmethod

from typing import Optional

from src.core.response.DefaultResponse import DefaultResponse
from src.core.response.AbortResponse import AbortResponse
from src.core.response.AbstractResponse import AbstractResponse
from src.const.globals import COMMAND_SEPARATOR_FUNCTION_PARTS, CORE_COMMAND_NAME, COMMAND_SEPARATOR_ADDON, \
    COMMAND_SEPARATOR_GROUP
from src.helper.args import convert_dict_to_args, convert_args_to_dict
from src.const.error import ERR_COMMAND_FILE_NOT_FOUND, ERR_COMMAND_CONTEXT
from src.helper.file import set_owner_for_path_and_ancestors, list_subdirectories
from src.helper.string import trim_leading, to_snake_case, to_kebab_case
from src.helper.system import get_user_or_sudo_user


class AbstractCommandProcessor:
    command: str
    command_args: list
    command_args_dict: dict
    command_function: str
    command_path: str
    command_type: str
    kernel = None
    match: Optional[re.Match] = None

    def __init__(self, kernel):
        self.kernel = kernel
        # Useful to store data about the current command execution.
        self.storage = {}

    def run(self, quiet: bool = False) -> AbstractResponse:
        import click

        # Get valid path.
        self.command_type = self.get_type()
        self.command_path: str = self.get_path()

        if not self.command_path or not os.path.isfile(self.command_path):
            if not quiet:
                self.kernel.error(ERR_COMMAND_FILE_NOT_FOUND, {
                    'command': self.command,
                    'path': self.command_path,
                })
            return AbortResponse()

        self.command_function = self.get_function(self.command_path)

        # Enforce sudo.
        if hasattr(self.command_function.callback, 'as_sudo') and os.geteuid() != 0:
            os.execvp('sudo', ['sudo'] + sys.argv)

        if isinstance(self.command_args, dict):
            self.command_args = convert_dict_to_args(self.command_function, self.command_args)

        self.command_args_dict = convert_args_to_dict(self.command_function, self.command_args)
        command_args = self.command_args

        middleware_args = {
            'processor': self,
        }

        self.kernel.exec_middlewares('run_pre', middleware_args)

        try:
            ctx = self.command_function.make_context('', command_args or [])
        # Click explicitly asked to exit, for example when using --help.
        except click.exceptions.Exit:
            return AbortResponse()
        except Exception as e:
            # Show error message
            self.kernel.error(
                ERR_COMMAND_CONTEXT,
                {
                    'function': self.command_function.callback.__name__,
                    'error': str(e)
                }
            )

        ctx.obj = self.kernel

        response = self.command_function.invoke(ctx)

        if not isinstance(response, AbstractResponse):
            response = DefaultResponse(response)

        self.kernel.exec_middlewares('run_post', middleware_args)

        return response

    def get_function(self, command_path: str) -> str:
        # Import module and load function.
        spec = importlib.util.spec_from_file_location(command_path, command_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        return getattr(
            module,
            self.get_function_name()
        )

    @classmethod
    @abstractmethod
    def get_pattern(cls) -> str:
        pass

    @staticmethod
    def get_commands_registry(kernel) -> dict:
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

    def set_command(self, command: str, args=None):
        if args is None:
            args = []

        self.command = command
        self.command_args = args

        self.match = self.build_match(command)

        return self.match

    @abstractmethod
    def get_path(self, subdir: str = None):
        pass

    def get_path_or_fail(self, subdir: str = None):
        path = self.get_path(subdir)

        if path is None:
            self.kernel.error(ERR_COMMAND_FILE_NOT_FOUND, {
                'command': self.command,
                'path': path,
            })

        return path

    def get_function_name(self) -> str | None:
        return to_snake_case(
            COMMAND_SEPARATOR_FUNCTION_PARTS.join(
                self.get_function_name_parts()
            )
        )

    @abstractmethod
    def get_function_name_parts(self) -> []:
        pass

    def build_full_command_from_function(self, function_or_command, args=None) -> str | None:
        if args is None:
            args = {}

        if isinstance(function_or_command, str):
            return function_or_command

        output = f'{CORE_COMMAND_NAME} '
        output += self.build_command_from_function(function_or_command)

        if len(args):
            output += ' ' + (' '.join(convert_dict_to_args(function_or_command, args)))

        return output

    def build_command_parts_from_function(self, function_name):
        """
        Returns the "default" format (addons style)
        """
        return function_name.split(COMMAND_SEPARATOR_FUNCTION_PARTS)[:3]

    def build_command_from_file_path(self, command_path: str) -> str | None:
        path_parts = command_path.split(os.sep)

        return self.build_command_from_parts([
            path_parts[-4],
            path_parts[-2],
            os.path.splitext(path_parts[-1])[0]
        ])

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

    def build_command_path(self, base_path, subdir: str | None, command_path):
        if subdir:
            base_path += f"{subdir}/"

        return os.path.join(base_path, 'command', command_path + '.py')

    def autocomplete_suggest(self, cursor: int, search_split: []) -> str | None:
        return None

    def suggest_arguments(self, command: str, search_params: []):
        self.set_command(
            command
        )

        # Command is not recognised
        if not self.match:
            return

        # File does not exist
        if not os.path.isfile(self.get_path()):
            return

        search_params = [val for val in search_params if val.startswith("-")]

        # Merge all params in a list,
        # but ignore already given args,
        # i.e : if -d is already given, do not suggest "-d" or "--default"
        function = self.get_function(
            self.get_path()
        )

        params = []
        for param in function.params:
            if any(opt in search_params for opt in param.opts):
                continue

            params += param.opts

        return ' '.join(params)

    def suggest_from_path(self, commands_path: str, search_string: str) -> []:
        commands = self.scan_commands_groups(commands_path)
        commands_names = []

        for command, command_data in commands.items():
            commands_names.append(command)

        # Ignore non relevant values
        commands_names = [
            name for name in commands_names if name.startswith(search_string)
        ]

        return commands_names

    def scan_commands_groups(self, directory: str):
        command_dict = {}

        if os.path.exists(directory):
            for group in list_subdirectories(directory):
                group_path = os.path.join(directory, group)
                command_dict.update(self.scan_commands(
                    group_path,
                    group,
                ))

        return command_dict

    def scan_commands(self, directory, group):
        """Scans the given directory for command files and returns a dictionary of found commands."""
        commands = {}
        for command in os.listdir(directory):
            if command.endswith('.py'):
                command_file = os.path.join(directory, command)
                test_file = os.path.realpath(os.path.join(directory, '../../tests/command', group, command))

                commands[self.build_command_from_file_path(command_file)] = {
                    'file': command_file,
                    'test': test_file if os.path.exists(test_file) else None
                }
        return commands
