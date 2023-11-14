import os
import sys
import yaml
from typing import Optional

from yaml import SafeLoader

from src.core.FunctionProperty import FunctionProperty
from src.helper.args import args_shift_one
from src.core.response.AbstractResponse import AbstractResponse
from src.core.response.NullResponse import NullResponse
from src.core.IOManager import IOManager
from src.core.Logger import Logger
from src.core.CommandRequest import CommandRequest
from src.core.AddonManager import AddonManager
from src.const.globals import \
    FILE_REGISTRY, COMMAND_TYPE_ADDON, KERNEL_RENDER_MODE_TERMINAL, \
    VERBOSITY_LEVEL_DEFAULT, VERBOSITY_LEVEL_QUIET, VERBOSITY_LEVEL_MEDIUM, VERBOSITY_LEVEL_MAXIMUM, \
    KERNEL_RENDER_MODE_JSON, ERR_COMMAND_FILE_NOT_FOUND
from src.core.command.resolver.AbstractCommandResolver import AbstractCommandResolver
from src.helper.file import list_subdirectories, remove_file_if_exists
from src.core.response.AbortResponse import AbortResponse


class Kernel:
    # Allow child classes override
    fast_mode: bool = False
    verbosity: int = VERBOSITY_LEVEL_DEFAULT
    tty: bool = os.isatty(0)

    def __init__(
            self,
            entrypoint_path: str,
            task_id: str | None = None
    ):
        self.root_request: None | CommandRequest = None
        self.current_request: None | CommandRequest = None
        self.current_response: None | AbstractResponse = None
        self.io = IOManager(self)
        self.logger = None
        self.post_exec: list = []
        self.previous_response: None | AbstractResponse = None
        self.registry: dict[str, Optional[str]] = {}
        self.sys_argv: list[str] = sys.argv.copy()
        self.task_id: str | None = task_id
        self.children: list = []
        self.default_render_mode = KERNEL_RENDER_MODE_TERMINAL
        self.parent_task_id: None | str = None
        self.tmp: dict = {}

        from src.decorator.alias import alias
        from src.decorator.as_sudo import as_sudo
        from src.decorator.test_command import test_command
        from src.decorator.command import command
        from src.decorator.no_log import no_log
        from src.decorator.verbosity import verbosity

        self.decorators = {
            'command': {
                'command': command,
                'test_command': test_command,
            },
            'properties': {
                'alias': alias,
                'as_sudo': as_sudo,
                'no_log': no_log,
                'verbosity': verbosity,
            }
        }

        # Initialize global variables.
        root_path = os.path.dirname(os.path.realpath(entrypoint_path)) + os.sep
        tmp_path = os.path.join(root_path, 'tmp') + os.sep

        self.path: dict = {
            'call': os.getcwd() + os.sep,
            'entrypoint': entrypoint_path,
            'root': root_path,
            'addons': os.path.join(root_path, 'addons') + os.sep,
            'core.cli': os.path.join(root_path, 'cli', 'wex'),
            'tmp': tmp_path,
            'templates': os.path.join(root_path, 'src', 'resources', 'templates') + os.sep,
            'task': os.path.join(tmp_path, 'task') + os.sep
        }

        # Check that script is called from a valid dir.
        self.get_path('call')

        # Initialize addons config
        self.addons = {}
        from addons.app.AppAddonManager import AppAddonManager
        definitions = {
            'app': AppAddonManager
        }

        for name in list_subdirectories(self.get_path('addons')):
            definition = definitions.get(name, AddonManager)
            self.addons[name]: AddonManager = definition(self, name=name)

        self.store_task_id()
        self.handle_core_args()

        # Create the logger after task_id created.
        self.logger: Logger = Logger(self)

        # Create resolvers
        from src.const.resolvers import COMMAND_RESOLVERS_CLASSES
        self.resolvers: dict = {
            class_definition.get_type(): class_definition(self)
            for class_definition in COMMAND_RESOLVERS_CLASSES
        }

        self.load_registry()

    def get_path(self, name: str, sub_dirs: list = None) -> str:
        """Get the path associated with the given name."""
        if name in self.path:
            base_path = self.path[name]

            if sub_dirs:
                return os.path.join(
                    base_path,
                    *sub_dirs
                ) + os.sep

            return base_path
        else:
            self.io.error(
                f'Core path not found {name}.'
            )

            sys.exit(1)

    def get_or_create_path(self, name: str) -> str:
        path = self.get_path(name)

        # Check if the directory exists, and if not, create it
        if not os.path.exists(path):
            try:
                os.makedirs(path)

                from src.helper.file import set_user_or_sudo_user_owner
                set_user_or_sudo_user_owner(path)
            except PermissionError:
                self.io.error(
                    f'Permission denied: Could not create {path}.'
                )

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

        if not self.fast_mode and len(self.post_exec):
            # Empty log message to keep visual stability
            # even executing post exec bash scripts.
            self.io.log_hide()
        # This is the real end as fast mode can't have post exec.
        else:
            self.logger.set_status_complete()

        if result is not None:
            self.io.print(result)

        if self.verbosity >= VERBOSITY_LEVEL_MAXIMUM:
            import shutil
            terminal_width, _ = shutil.get_terminal_size()

            self.io.log(
                '_' * terminal_width,
                increment=-self.io.log_indent,
                verbosity=VERBOSITY_LEVEL_MAXIMUM)

    def call_command(
            self,
            command: str,
            command_args: dict | list | None = None,
            render_mode: str | None = None):

        render_mode = render_mode or self.default_render_mode

        response = self.run_command(
            command,
            command_args or [],
            render_mode=render_mode
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

        printed = response.print(
            render_mode or self.default_render_mode
        ) if response else None

        if render_mode == KERNEL_RENDER_MODE_JSON:
            import json

            return json.dumps(printed)

        return printed

    def run_command(self,
                    command: str,
                    args: dict | list = None,
                    quiet: bool = False,
                    render_mode: str | None = None) -> AbstractResponse:
        request = self.create_command_request(command, args)

        if not request and not quiet:
            self.io.error(
                "Invalid command format. Must be in the format 'addon::group/name' or 'group/name', got : {command}",
                {
                    'command': command
                }, trace=False
            )

        request.quiet = quiet

        return self.render_request(request, render_mode)

    def run_function(self,
                     function,
                     args: dict | list = None,
                     type: str = COMMAND_TYPE_ADDON,
                     quiet: bool = False,
                     render_mode: str | None = None) -> AbstractResponse:
        resolver = self.get_command_resolver(type)

        request = self.create_command_request(
            resolver.build_command_from_function(function),
            args
        )

        request.quiet = quiet

        return self.render_request(request, render_mode)

    def render_request(self,
                       request,
                       render_mode: str | None = None) -> AbstractResponse:
        # Save unique root request
        self.root_request = self.root_request if self.root_request else request

        if not request.runner:
            if not request.quiet:
                self.io.error(ERR_COMMAND_FILE_NOT_FOUND, {
                    'command': request.command,
                    'path': request.path,
                }, trace=False)

            return NullResponse(self)

        # Ensure command has proper type defined,
        # i.e. check if command file location matches with defined command type
        # and prevent it to be resolved with the wrong resolver.
        command_type = request.runner.get_command_type()
        resolver_type = request.resolver.get_type()
        if command_type != resolver_type:
            message = ("Command type \"{command_type}\" does not match with resolver type \"{resolver_type}\" for "
                       "command {command}")

            self.io.error(message, {
                'command': request.command,
                'command_type': command_type,
                'resolver_type': resolver_type,
            })

            return AbortResponse(self, reason=message)

        # Enforce sudo.
        if FunctionProperty.has_property(request.function, 'as_sudo') and os.geteuid() != 0:
            self.logger.append_event('EVENT_SWITCH_SUDO')
            # Mask printed logs as it may not be relevant.
            self.io.log_hide()
            # Uses the original argv argument to ignore any changes on it.
            os.execvp('sudo', ['sudo', sys.executable] + sys.argv)

        return request.resolver.render_request(
            request,
            render_mode or self.default_render_mode
        )

    def task_file_path(self, type: str, task_id: str | None = None):
        return os.path.join(self.get_or_create_path('task'), f"{task_id or self.task_id}.{type}")

    def task_file_load(
            self,
            type: str,
            task_id: str | None = None,
            delete_after_read: bool = True,
            create_if_missing: bool = True,
            default=''):
        """
        Load the content of a file and optionally delete the file after reading. If the file does not exist
        and `create_if_missing` is True, a new file will be created with the `default` content.
        """
        file_path = self.task_file_path(type, task_id)

        # Check if the file exists
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read()

            # Delete the file after reading, if requested
            if delete_after_read:
                os.remove(file_path)

            return content
        else:
            # If the file doesn't exist and 'create_if_missing' is True, create the file
            if create_if_missing:
                self.task_file_write(
                    type,
                    body=default
                )

                # Return the default content as the file content
                return default
            else:
                # If not creating a file, just return the default
                return default

    def task_file_write(
            self,
            type: str,
            body: str,
            task_id: str | None = None,
            replace: bool = False):
        from src.helper.file import set_user_or_sudo_user_owner
        path = self.task_file_path(type, task_id=task_id)

        with open(path, 'w' if replace else 'a') as f:
            f.write(body)

            set_user_or_sudo_user_owner(path)

            return path

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
                response = hook_method(**args)

                if response:
                    return response

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
        if self.task_id:
            return

        task_id = self.sys_argv[1] if len(self.sys_argv) > 1 else None
        if task_id is None:
            self.io.error(
                'Please use the "bash ./cli/wex" file to run wex script.',
                trace=False
            )
            sys.exit(1)

        self.task_id = self.sys_argv[1]

    def handle_core_args(self):
        if args_shift_one(self.sys_argv, 'fast-mode', True) is not None:
            self.fast_mode = True

        if args_shift_one(self.sys_argv, 'quiet', True) is not None:
            self.verbosity = VERBOSITY_LEVEL_QUIET

        if args_shift_one(self.sys_argv, 'vv', True) is not None:
            self.verbosity = VERBOSITY_LEVEL_MEDIUM

        if args_shift_one(self.sys_argv, 'vvv', True) is not None:
            self.verbosity = VERBOSITY_LEVEL_MAXIMUM

        value = args_shift_one(self.sys_argv, 'log-indent')
        if value is not None:
            self.io.log_indent = int(value)

        # Setting verbosity will disable logging frame.
        value = args_shift_one(self.sys_argv, 'log-length')
        if not sys.stdout.isatty() or self.verbosity != VERBOSITY_LEVEL_DEFAULT:
            value = 0

        if value is not None:
            self.io.log_length = int(value)

        value = args_shift_one(self.sys_argv, 'render-mode')
        if value is not None:
            self.default_render_mode = value

        value = args_shift_one(self.sys_argv, 'parent-task-id')
        if value is not None:
            self.parent_task_id = value

        # There is a task id redirection
        value = args_shift_one(self.sys_argv, 'kernel-task-id')
        if value:
            self.task_file_write(
                'task-redirect',
                value,
                replace=True
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

    def apply_command_decorator(
            self,
            function,
            group: str,
            name: str,
            options: dict | None = None):
        if group in self.decorators and name in self.decorators[group]:
            decorator = self.decorators[group][name]
            options = options or {}

            return decorator(
                **options
            )(function)
        else:
            self.io.error(f'Missing decorator {group}.{name}')
