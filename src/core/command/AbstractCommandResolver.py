import importlib.util
import os
import re
import sys
from abc import abstractmethod

from src.decorator.command import COMMAND_HELP_PARAMS
from src.core.response.FunctionResponse import FunctionResponse
from src.core.response.DefaultResponse import DefaultResponse
from src.core.response.AbortResponse import AbortResponse
from src.core.response.AbstractResponse import AbstractResponse
from src.const.globals import COMMAND_SEPARATOR_FUNCTION_PARTS, CORE_COMMAND_NAME, COMMAND_SEPARATOR_ADDON, \
    COMMAND_SEPARATOR_GROUP
from src.helper.args import convert_dict_to_args, convert_dict_to_snake_dict
from src.const.error import ERR_COMMAND_FILE_NOT_FOUND, ERR_COMMAND_CONTEXT
from src.helper.file import set_owner_for_path_and_ancestors, list_subdirectories
from src.helper.string import trim_leading, to_snake_case, to_kebab_case
from src.helper.system import get_user_or_sudo_user

from src.core.CommandRequest import CommandRequest


class AbstractCommandResolver:
    def __init__(self, kernel):
        self.kernel = kernel

    def render_request(self, request: CommandRequest, render_mode: str) -> AbstractResponse:
        import click

        self.kernel.logger.append_request(request)

        if not request.function and (not request.path or not os.path.isfile(request.path)):
            if not request.quiet:
                self.kernel.io.error(ERR_COMMAND_FILE_NOT_FOUND, {
                    'command': request.command,
                    'path': request.path,
                })

            return AbortResponse(self.kernel, reason=ERR_COMMAND_FILE_NOT_FOUND)

        # Enforce sudo.
        if hasattr(request.function.callback, 'as_sudo') and os.geteuid() != 0:
            # Mask printed logs as it may not be relevant.
            self.kernel.io.log_hide()
            # Uses the original argv argument to ignore any changes on it.
            os.execvp('sudo', ['sudo'] + sys.argv)

        middleware_args = {
            'request': request,
        }

        self.kernel.exec_middlewares('run_pre', middleware_args)

        try:
            ctx = request.function.make_context('', request.args.copy() or [])
        # Click explicitly asked to exit, for example when using --help.
        except click.exceptions.Exit:
            return AbortResponse(self.kernel, reason='INFO_COMMAND')
        except Exception as e:
            # Show error message
            self.kernel.io.error(
                ERR_COMMAND_CONTEXT,
                {
                    'function': request.function.callback.__name__,
                    'error': str(e)
                }
            )

        # Remove click params which have been defined only
        # to be shown in help section, but are used outside function
        for arg in COMMAND_HELP_PARAMS:
            if arg in ctx.params:
                del ctx.params[arg]

        # Defines kernel as mais class to provide with pass_obj option.
        ctx.obj = self.kernel

        response = self.wrap_response(
            request.function.invoke(ctx)
        )

        middleware_args['response'] = response

        response = response.render(request, render_mode)

        self.kernel.exec_middlewares('run_post', middleware_args)

        return response

    def wrap_response(self, response) -> AbstractResponse:
        if callable(response):
            return FunctionResponse(self.kernel, response)
        if not isinstance(response, AbstractResponse):
            return DefaultResponse(self.kernel, response)

        return response

    def get_function_from_request(self, request: CommandRequest) -> str:
        return self.get_function(
            request.path,
            list(request.match.groups())
        )

    def get_function(self, command_path: str, parts: list) -> str:
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

    def create_command_request(self, command: str, args: None | list = None):
        args = args or []

        request = CommandRequest(
            self,
            command,
            args
        )

        return request

    @classmethod
    def resolve_alias(cls, kernel, command: str) -> str:
        registry = cls.get_commands_registry(kernel)
        for item in registry:
            if command in registry[item]['alias']:
                return item
        return command

    @classmethod
    def supports(cls, kernel, command: str) -> bool:
        command = cls.resolve_alias(kernel, command)

        if cls.build_match(command):
            return True

        return False

    @abstractmethod
    def build_path(self, request: CommandRequest, subdir: str = None):
        pass

    def build_path_or_fail(self, request: CommandRequest, subdir: str = None):
        path = self.build_path(request, subdir)

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

    def build_full_command_from_function(self, function_or_command, args: dict = None) -> str | None:
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

    def build_command_path(self, base_path, subdir: str | None, command_path):
        if subdir:
            base_path += f"{subdir}/"

        return os.path.join(base_path, 'command', command_path + '.py')

    def autocomplete_suggest(self, cursor: int, search_split: []) -> str | None:
        return None

    def suggest_arguments(self, command: str, search_params: []):
        request = self.create_command_request(
            command
        )

        # Command is not recognised
        if not request.function:
            return

        search_params = [val for val in search_params if val.startswith("-")]

        params = []
        for param in request.function.params:
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

                    aliases_raw = function.callback.aliases if hasattr(function.callback, 'aliases') else []
                    aliases = []
                    for alias in aliases_raw:
                        aliases.append(self.build_alias(function, alias))

                    commands[self.build_command_from_parts(parts)] = {
                        'file': command_file,
                        'test': test_file if os.path.exists(test_file) else None,
                        'alias': aliases
                    }
        return commands
