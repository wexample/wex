import os
import sys
from typing import TYPE_CHECKING, Any, Callable, Dict, List, NoReturn, Optional

from addons.app.AppAddonManager import AppAddonManager
from addons.app.command.env.get import _app__env__get
from src.const.globals import (
    COMMAND_TYPE_ADDON,
    FILE_REGISTRY,
    KERNEL_RENDER_MODE_TERMINAL,
    VERBOSITY_LEVEL_DEFAULT,
    VERBOSITY_LEVEL_MAXIMUM,
    VERBOSITY_LEVEL_MEDIUM,
    VERBOSITY_LEVEL_QUIET,
)
from src.core.AddonManager import AddonManager
from src.core.BaseClass import BaseClass
from src.core.file.KernelDirectoryStructure import KernelDirectoryStructure
from src.core.file.KernelRegistryFileStructure import KernelRegistryFileStructure
from src.core.file.KernelSystemRootDirectoryStructure import (
    KernelSystemRootDirectoryStructure,
)
from src.core.IOManager import IOManager
from src.core.Logger import Logger
from src.core.response.NullResponse import NullResponse
from src.decorator.alias import alias
from src.decorator.as_sudo import as_sudo
from src.decorator.attach import attach
from src.decorator.command import command
from src.decorator.no_log import no_log
from src.decorator.test_command import test_command
from src.decorator.verbosity import verbosity
from src.helper.args import args_shift_one
from src.helper.file import file_list_subdirectories, file_remove_file_if_exists

if TYPE_CHECKING:
    from src.const.types import (
        CoreCommandArgsList,
        CoreCommandString,
        OptionalCoreCommandArgsListOrDict,
        StringsList,
    )
    from src.core.command.resolver.AbstractCommandResolver import (
        AbstractCommandResolver,
    )
    from src.core.command.ScriptCommand import ScriptCommand
    from src.core.CommandRequest import CommandRequest
    from src.core.ErrorMessage import ErrorMessage
    from src.core.file.AbstractFileSystemStructure import AbstractFileSystemStructure
    from src.core.response.AbortResponse import AbortResponse
    from src.core.response.AbstractResponse import AbstractResponse


class Kernel(BaseClass):
    # Allow child classes override
    fast_mode: bool = False
    verbosity: int = VERBOSITY_LEVEL_DEFAULT
    tty: bool = os.isatty(0)
    registry_structure: "KernelRegistryFileStructure"

    def __init__(self, entrypoint_path: str, task_id: str | None = None) -> None:
        self._task_id: str | None = task_id

        self.fast_mode_previous: Optional[bool] = None
        self.root_request: Optional["CommandRequest"] = None
        self.current_request: Optional["CommandRequest"] = None
        self.current_response: Optional["AbstractResponse"] = None
        self.io = IOManager(self)
        self.post_exec: StringsList = []
        self.previous_response: Optional["AbstractResponse"] = None
        self.sys_argv: list[str] = sys.argv.copy()
        self.default_render_mode = KERNEL_RENDER_MODE_TERMINAL
        self.parent_task_id: None | str = None
        self.tmp: Dict[str, str] = {}

        self.decorators: Dict[str, Dict[str, Callable[..., Any]]] = {
            "command": {
                "command": command,
                "test_command": test_command,
            },
            "properties": {
                "alias": alias,
                "attach": attach,
                "as_sudo": as_sudo,
                "no_log": no_log,
                "verbosity": verbosity,
            },
        }

        self.store_task_id()

        # Initialize global variables.
        root_path = os.path.dirname(os.path.realpath(entrypoint_path)) + os.sep
        tmp_path = os.path.join(root_path, "tmp") + os.sep

        # Handle calling from a non-existing dir.
        try:
            call_dir = os.getcwd() + os.sep
        except FileNotFoundError:
            raise Exception("You are in a non existing directory")

        self.path: Dict[str, str] = {
            "call": call_dir,
            "entrypoint": entrypoint_path,
            "root": root_path,
            "addons": os.path.join(root_path, "addons") + os.sep,
            "core.cli": os.path.join(root_path, "cli", "wex"),
            "tmp": tmp_path,
            "templates": os.path.join(root_path, "src", "resources", "templates")
            + os.sep,
            "task": os.path.join(tmp_path, "task") + os.sep,
        }

        self.directory = KernelDirectoryStructure(
            path=root_path,
        )

        self.system_root_directory = KernelSystemRootDirectoryStructure(
            env=_app__env__get(self, root_path),
            path=os.sep,
        )

        # Create logger after task id and locations set.
        self.logger: Logger = Logger(self)

        # Initialize addons config
        self.addons: Dict[str, AddonManager] = {}
        definitions = {"app": AppAddonManager}

        for name in file_list_subdirectories(self.get_path("addons")):
            definition = definitions.get(name, AddonManager)
            self.addons[name] = definition(self, name=name)

        # Display directory structure error if exists
        self.file_structure_display_errors(self.directory)

        # Create resolvers
        from src.const.resolvers import COMMAND_RESOLVERS_CLASSES

        self.resolvers: Dict[str, AbstractCommandResolver] = {
            class_definition.get_type(): class_definition(self)
            for class_definition in COMMAND_RESOLVERS_CLASSES
        }

        self.load_registry()

        self.handle_core_args()

    def get_path(
        self, name: str, sub_dirs: Optional[List[str]] = None
    ) -> str | NoReturn:
        """Get the path associated with the given name."""
        if name in self.path:
            base_path = self.path[name]

            if sub_dirs:
                return os.path.join(base_path, *sub_dirs) + os.sep

            return base_path
        else:
            self.io.error(f"Core path not found {name}.")

            sys.exit(1)

    def get_or_create_path(self, name: str) -> str:
        path = self.get_path(name)

        # Check if the directory exists, and if not, create it
        if not os.path.exists(path):
            try:
                os.makedirs(path)

                from src.helper.file import file_set_user_or_sudo_user_owner

                file_set_user_or_sudo_user_owner(path)
            except PermissionError:
                self.io.error(f"Permission denied: Could not create {path}.")

                sys.exit(1)

        return path

    def load_registry(self) -> None:
        self.registry_structure = KernelRegistryFileStructure(
            self, os.path.join(self.directory.shortcuts["tmp"].path, FILE_REGISTRY)
        )

        # Load registry if empty
        if not self.registry_structure.exists():
            self.registry_structure.build()

        # Check again
        self.registry_structure.should_exist = True
        self.registry_structure.checkup()

    def trace(self, _exit: bool = True) -> Optional[NoReturn]:
        import traceback

        for line in traceback.format_stack():
            self.io.print(line.strip())

        if _exit:
            sys.exit(1)

        return None

    def call(self) -> None:
        """
        Main entrypoint from bash call.
        May never be called by an internal script.
        :return:
        """

        # No arg found except process id
        if not len(self.sys_argv) > 2:
            return

        command: str = self.sys_argv[2]
        command_args: CoreCommandArgsList = self.sys_argv[3:]

        result = self.call_command(command, command_args)

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
                "_" * terminal_width,
                increment=-self.io.log_indent,
                verbosity=VERBOSITY_LEVEL_MAXIMUM,
            )

    def call_command(
        self,
        command: "CoreCommandString",
        command_args: Optional["OptionalCoreCommandArgsListOrDict"] = None,
        render_mode: str | None = None,
    ) -> Optional[str]:
        render_mode = render_mode or self.default_render_mode

        response = self.run_command(
            command, command_args or [], render_mode=render_mode
        )

        # Store command to execute after kernel execution,
        # it should be set at the last moment,
        # to avoid execution if any error happened before
        for post_command in self.post_exec:
            from src.helper.command import command_to_string

            self.task_file_write(
                "post-exec",
                command_to_string(post_command) + os.linesep,
            )

        return (
            response.print_wrapped(render_mode or self.default_render_mode)
            if response
            else None
        )

    def run_command(
        self,
        command: "CoreCommandString",
        args: Optional["OptionalCoreCommandArgsListOrDict"] = None,
        quiet: bool = False,
        render_mode: str | None = None,
        fast_mode: Optional[bool] = None,
    ) -> "AbstractResponse":
        self.set_temporary_fast_mode(fast_mode)

        result = self.render_request(
            self.create_command_request(command=command, args=args, quiet=quiet),
            render_mode,
        )

        self.revert_temporary_fast_mode(fast_mode)

        return result

    def revert_temporary_fast_mode(self, value: Optional[bool]) -> None:
        """Revert fast mode status only if value have been forced"""
        if value is not None:
            self.fast_mode = self.fast_mode_previous or self.fast_mode

    def set_temporary_fast_mode(self, value: Optional[bool]) -> None:
        self.fast_mode_previous = None

        if value is not None:
            self.fast_mode_previous = self.fast_mode
            self.fast_mode = value

    def run_function(
        self,
        function: "ScriptCommand",
        args: Optional["OptionalCoreCommandArgsListOrDict"] = None,
        type: str = COMMAND_TYPE_ADDON,
        quiet: bool = False,
        render_mode: str | None = None,
        fast_mode: Optional[bool] = None,
    ) -> "AbstractResponse":
        if not self.has_command_resolver(type):
            return self.create_abort_response(
                message=f'Resolver not found for type "{type}"'
            )

        self.set_temporary_fast_mode(fast_mode)

        request = self.create_command_request(
            command=self.get_command_resolver(type).build_command_from_function(
                function
            ),
            args=args,
            quiet=quiet,
        )

        result = self.render_request(request, render_mode)

        self.revert_temporary_fast_mode(fast_mode)

        return result

    def create_abort_response(self, message: str) -> "AbstractResponse":
        from src.core.response.AbortResponse import AbortResponse

        return AbortResponse(self, reason=message)

    def render_request(
        self, request: "CommandRequest", render_mode: str | None = None
    ) -> "AbstractResponse":
        # Save unique root request
        self.root_request = self.root_request if self.root_request else request

        if not request._runner:
            if not request.quiet:
                self.io.error(
                    'Command file not found when rendering, command {command}, in path "{path}"',
                    {
                        "command": str(request._string_command),
                        "path": str(request._path),
                    },
                    trace=False,
                )

            return NullResponse(self)

        # Ensure command has proper type defined,
        # i.e. check if command file location matches with defined command type
        # and prevent it to be resolved with the wrong resolver.
        command_type = request.get_runner().get_command_type()
        resolver_type = request.resolver.get_type()
        if command_type != resolver_type:
            message = (
                'Command type "{command_type}" does not match with resolver type "{resolver_type}" for '
                "command {command}"
            )

            self.io.error(
                message,
                {
                    "command": request.get_string_command(),
                    "command_type": command_type,
                    "resolver_type": resolver_type,
                },
            )

            return AbortResponse(self, reason=message)

        # Enforce sudo.
        if request.get_script_command().as_sudo and os.geteuid() != 0:
            self.logger.append_event("EVENT_SWITCH_SUDO")
            # Mask printed logs as it may not be relevant.
            self.io.log_hide()
            # Uses the original argv argument to ignore any changes on it.
            os.execvp("sudo", ["sudo", sys.executable] + sys.argv)

        return request.resolver.render_request(
            request, render_mode or self.default_render_mode
        )

    def task_file_path(self, type: str, task_id: str | None = None) -> str:
        return os.path.join(
            self.get_or_create_path("task"), f"{task_id or self.get_task_id()}.{type}"
        )

    def task_file_load(
        self,
        type: str,
        task_id: str | None = None,
        delete_after_read: bool = True,
        create_if_missing: bool = True,
        default: str = "",
    ) -> str:
        """
        Load the content of a file and optionally delete the file after reading. If the file does not exist
        and `create_if_missing` is True, a new file will be created with the `default` content.
        """
        file_path = self.task_file_path(type, task_id)

        # Check if the file exists
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                content = f.read()

            # Delete the file after reading, if requested
            if delete_after_read:
                os.remove(file_path)

            return content
        else:
            # If the file doesn't exist and 'create_if_missing' is True, create the file
            if create_if_missing:
                self.task_file_write(type, body=default)

                # Return the default content as the file content
                return default
            else:
                # If not creating a file, just return the default
                return default

    def task_file_write(
        self, type: str, body: str, task_id: str | None = None, replace: bool = False
    ) -> str:
        from src.helper.file import file_set_user_or_sudo_user_owner

        path = self.task_file_path(type, task_id=task_id)

        with open(path, "w" if replace else "a") as f:
            f.write(body)

            file_set_user_or_sudo_user_owner(path)

            return path

    def guess_command_type(self, command: "CoreCommandString") -> Optional[str]:
        for type in self.resolvers:
            if self.resolvers[type].supports(command):
                return type
        return None

    def hook_addons(self, name: str, args: Optional[Dict[str, Any]] = None) -> None:
        args = args or {}

        hook = f"hook_{name}"
        # Init addons
        for addon in self.addons:
            addon_manager = self.addons[addon]
            # Dynamically call the hook method if it exists
            hook_method = getattr(addon_manager, hook, None)

            if hook_method:
                response = hook_method(**args)

                if response:
                    return

    def has_command_resolver(self, type: str) -> bool:
        return type in self.resolvers

    def get_command_resolver(self, type: str) -> "AbstractCommandResolver":
        return self.resolvers[type]

    def create_command_request(
        self,
        command: "CoreCommandString",
        args: Optional["OptionalCoreCommandArgsListOrDict"] = None,
        quiet: bool = False,
    ) -> "CommandRequest" | NoReturn:
        command_type = self.guess_command_type(command)

        if command_type:
            request = self.get_command_resolver(command_type).create_command_request(
                command, args
            )
            request.quiet = quiet

            return request

        if not quiet:
            self.io.error(
                "Invalid command format. Must be in the format 'addon::group/name' or 'group/name', got : {command}",
                {"command": command},
                trace=False,
            )

        assert False

    def get_task_id(self) -> str:
        self._validate__should_not_be_none(self._task_id)
        assert self._task_id is not None

        return self._task_id

    def set_task_id(self, task_id: str) -> None:
        self._task_id = task_id

    def store_task_id(self) -> Optional[NoReturn]:
        task_id = self.sys_argv[1] if len(self.sys_argv) > 1 else None
        if task_id is None:
            self.io.error(
                'Please use the "bash ./cli/wex" file to run wex script.', trace=False
            )

        self.set_task_id(self.sys_argv[1])
        return None

    def handle_core_args(self) -> None:
        if args_shift_one(self.sys_argv, "fast-mode", True) is not None:
            self.fast_mode = True

        if args_shift_one(self.sys_argv, "quiet", True) is not None:
            self.verbosity = VERBOSITY_LEVEL_QUIET

        if args_shift_one(self.sys_argv, "vv", True) is not None:
            self.verbosity = VERBOSITY_LEVEL_MEDIUM

        if args_shift_one(self.sys_argv, "vvv", True) is not None:
            self.verbosity = VERBOSITY_LEVEL_MAXIMUM

        value: str | bool | int | None
        value = args_shift_one(self.sys_argv, "log-indent")
        if value is not None:
            self.io.log_indent = int(value)

        # Setting verbosity will disable logging frame.
        value = args_shift_one(self.sys_argv, "log-length")
        if not sys.stdout.isatty() or self.verbosity != VERBOSITY_LEVEL_DEFAULT:
            value = 0

        if value is not None:
            self.io.log_length = int(value)

        value = args_shift_one(self.sys_argv, "render-mode")
        if isinstance(value, str):
            self.default_render_mode = value

        value = args_shift_one(self.sys_argv, "parent-task-id")
        if isinstance(value, str):
            self.parent_task_id = value

        # There is a task id redirection
        value = args_shift_one(self.sys_argv, "kernel-task-id")
        if isinstance(value, str):
            self.task_file_write("task-redirect", value, replace=True)

            self.set_task_id(value)

            # Cleanup task files to avoid loops.
            file_remove_file_if_exists(self.task_file_path("post-exec"))

    def file_structure_display_errors(
        self, file_system_structure: "AbstractFileSystemStructure"
    ) -> None:
        errors = file_system_structure.get_all_errors()
        if len(errors):
            error: "ErrorMessage" = errors[0]

            self.io.error(error.message, error.parameters)
