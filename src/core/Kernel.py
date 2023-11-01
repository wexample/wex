import os
import sys
import yaml
from typing import Optional

from yaml import SafeLoader

from addons.app.AppAddonManager import AppAddonManager
from src.const.resolver import COMMAND_RESOLVERS_CLASSES
from src.helper.args import arg_shift
from src.core.response.AbstractResponse import AbstractResponse
from src.core.IOManager import IOManager
from src.core.Logger import Logger
from src.core.CommandRequest import CommandRequest
from src.core.AddonManager import AddonManager
from src.const.error import \
    ERR_ARGUMENT_COMMAND_MALFORMED, ERR_UNEXPECTED
from src.const.globals import \
    FILE_REGISTRY, COMMAND_TYPE_ADDON, KERNEL_RENDER_MODE_CLI, \
    VERBOSITY_LEVEL_DEFAULT, VERBOSITY_LEVEL_QUIET, VERBOSITY_LEVEL_MEDIUM, VERBOSITY_LEVEL_MAXIMUM
from src.core.command.AbstractCommandResolver import AbstractCommandResolver
from src.helper.file import list_subdirectories, remove_file_if_exists

ADDONS_DEFINITIONS = {
    'app': AppAddonManager
}


class Kernel:
    # Allow child classes override
    fast_mode: bool = False
    verbosity: int = VERBOSITY_LEVEL_DEFAULT

    def __init__(self, entrypoint_path: str):
        self.current_request: None | CommandRequest = None
        self.current_response: None | AbstractResponse = None
        self.io = IOManager(self)
        self.post_exec: list = []
        # Use a clone to keep original command.
        self.previous_response: None | AbstractResponse = None
        self.registry: dict[str, Optional[str]] = {}
        self.sys_argv: list[str] = sys.argv.copy()
        self.task_id: str | None = None

        # Initialize global variables.
        root_path = os.path.dirname(os.path.realpath(entrypoint_path)) + os.sep
        tmp_path = os.path.join(root_path, 'tmp') + os.sep

        self.path: dict = {
            'call': os.getcwd() + os.sep,
            'root': root_path,
            'addons': os.path.join(root_path, 'addons') + os.sep,
            'core.cli': os.path.join(root_path, 'cli', 'wex'),
            'tmp': tmp_path,
            'log': os.path.join(tmp_path, 'log') + os.sep,
            'templates': os.path.join(root_path, 'src', 'resources', 'templates') + os.sep
        }

        # Check that script is called from a valid dir.
        self.get_path('call')

        # Initialize addons config
        self.addons = {}
        for name in list_subdirectories(self.get_path('addons')):
            definition = ADDONS_DEFINITIONS.get(name, AddonManager)
            self.addons[name]: AddonManager = definition(self, name=name)

        self.store_task_id()
        self.handle_core_args()

        # Create the logger after task_id created.
        self.logger: Logger = Logger(self)

        # Create resolvers
        self.resolvers: dict = {
            class_definition.get_type(): class_definition(self)
            for class_definition in COMMAND_RESOLVERS_CLASSES
        }

        self.load_registry()

    def get_path(self, name: str) -> str:
        """Get the path associated with the given name."""
        if name in self.path:
            return self.path[name]
        else:
            self.io.error(
                ERR_UNEXPECTED,
                {
                    'error': f'Kernel path not found {name}.'
                }
            )

            sys.exit(1)

    def get_or_create_path(self, name: str) -> str:
        path = self.get_path(name)

        # Check if the directory exists, and if not, create it
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except PermissionError:
                self.io.error(
                    ERR_UNEXPECTED,
                    {
                        'error': f'Permission denied: Could not create {path}.'
                    }
                )
                self.io['error'](f"Permission denied: Could not create {path}.")
                sys.exit(1)

        return path

    def load_registry(self):
        path_registry = f"{self.get_or_create_path('tmp')}{FILE_REGISTRY}"

        # Load registry if empty
        if not os.path.exists(path_registry):
            self.rebuild()

        with open(path_registry) as f:
            self.registry = yaml.load(f, SafeLoader)

    def rebuild(self, test: bool = False):
        from addons.core.command.registry.build import _core__registry__build

        _core__registry__build(self, test)

    def trace(self, _exit: bool = True):
        import traceback

        for line in traceback.format_stack():
            self.io.print(line.strip())

        if _exit:
            exit(1)

    def call(self):
        """
        Main entrypoint from bash call.
        May never be called by an internal script.
        :return:
        """

        # No arg found except process id
        if not len(self.sys_argv) > 2:
            return

        command: str = self.sys_argv[2]
        command_args: [] = self.sys_argv[3:]

        result = self.call_command(
            command,
            command_args
        )

        # Empty log message to keep visual stability
        # even executing post exec bash scripts.
        if not self.fast_mode and len(self.post_exec):
            self.io.log_hide()

        if result is not None:
            self.io.print(result)

        self.io.log(
            '_' * 60,
            increment=-self.io.log_indent,
            verbosity=VERBOSITY_LEVEL_MAXIMUM)

    def call_command(self, command: str, command_args: dict | list | None = None):
        response = self.run_command(
            command,
            command_args or []
        )

        # Store command to execute after kernel execution,
        # it should be set at the last moment,
        # to avoid execution if any error happened before
        for post_command in self.post_exec:
            from src.helper.command import command_to_string

            self.task_file_write(
                'post-exec',
                command_to_string(post_command) + '\n',
            )

        return response.print() if response else None

    def run_command(self,
                    command: str,
                    args: dict | list = None,
                    quiet: bool = False) -> AbstractResponse:
        request = self.create_command_request(command, args)

        if not request and not quiet:
            self.io.error(ERR_ARGUMENT_COMMAND_MALFORMED, {
                'command': command
            })

        request.quiet = quiet

        return self.render_request(request)

    def run_function(self,
                     function,
                     args: dict | list = None,
                     type: str = COMMAND_TYPE_ADDON,
                     quiet: bool = False) -> AbstractResponse:
        resolver = self.get_command_resolver(type)

        request = self.create_command_request(
            resolver.build_command_from_function(function),
            args
        )

        request.quiet = quiet

        return self.render_request(request)

    def render_request(self, request) -> AbstractResponse:
        return request.resolver.render_request(request, KERNEL_RENDER_MODE_CLI)

    def task_file_path(self, type: str):
        task_dir = os.path.join(self.get_or_create_path('tmp'), 'task')
        os.makedirs(task_dir, exist_ok=True)
        return os.path.join(task_dir, f"{self.task_id}.{type}")

    def task_file_load(self, type: str):
        file_path = self.task_file_path(type)

        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return f.read()
        else:
            return None

    def task_file_write(self, type: str, body: str, replace: bool = False):
        from src.helper.file import set_user_or_sudo_user_owner
        path = self.task_file_path(type)

        with open(path, 'w' if replace else 'a') as f:
            f.write(body)

            set_user_or_sudo_user_owner(path)

    def guess_command_type(self, command: str) -> str | None:
        for type in self.resolvers:
            if self.resolvers[type].supports(command):
                return type

    def hook_addons(self, name: str, args=None):
        if args is None:
            args = {}

        hook = f'hook_{name}'
        # Init addons
        for addon in self.addons:
            addon_manager = self.addons[addon]
            # Dynamically call the hook method if it exists
            hook_method = getattr(addon_manager, hook, None)
            if hook_method:
                hook_method(**args)

    def get_command_resolver(self, type: str) -> AbstractCommandResolver | None:
        return self.resolvers[type] or None

    def create_command_request(self, command: str, args: dict | list = None) -> CommandRequest | None:
        type = self.guess_command_type(command)

        if type:
            resolver = self.get_command_resolver(type)

            if resolver:
                return resolver.create_command_request(command, args)

        return None

    def store_task_id(self):
        task_id = self.sys_argv[1] if len(self.sys_argv) > 1 else None
        if task_id is None:
            self.io.error(
                ERR_UNEXPECTED,
                {
                    'error': 'Please use the "bash ./cli/wex" file to run wex script.'
                }
            )
            sys.exit(1)

        self.task_id = self.sys_argv[1]

    def handle_core_args(self):
        if arg_shift(self.sys_argv, 'fast-mode', True) is not None:
            self.fast_mode = True

        if arg_shift(self.sys_argv, 'quiet', True) is not None:
            self.verbosity = VERBOSITY_LEVEL_QUIET

        if arg_shift(self.sys_argv, 'vv', True) is not None:
            self.verbosity = VERBOSITY_LEVEL_MEDIUM

        if arg_shift(self.sys_argv, 'vvv', True) is not None:
            self.verbosity = VERBOSITY_LEVEL_MAXIMUM

        value = arg_shift(self.sys_argv, 'log-indent')
        if value is not None:
            self.io.log_indent = int(value)

        # Setting verbosity will disable logging frame.
        if not sys.stdout.isatty() or self.verbosity != VERBOSITY_LEVEL_DEFAULT:
            value = 0
        else:
            value = arg_shift(self.sys_argv, 'log-length')

        if value is not None:
            self.io.log_length = int(value)

        # There is a task id redirection
        value = arg_shift(self.sys_argv, 'kernel-task-id')
        if value:
            self.task_file_write(
                'task-redirect',
                value,
                True
            )

            self.task_id = value

            # Cleanup task files to avoid loops.
            remove_file_if_exists(
                self.task_file_path('post-exec')
            )

    def load_env(self):
        from dotenv import load_dotenv
        # Load .env file to get API token
        load_dotenv(dotenv_path=self.get_path('root') + '.env')
