import os
import sys
from typing import TYPE_CHECKING, Any, List, NoReturn, Optional, TypedDict

from src.const.globals import (
    COLOR_CYAN,
    COLOR_GRAY,
    COLOR_GREEN,
    COLOR_RED,
    COLOR_RESET,
    COMMAND_TYPE_ADDON,
    VERBOSITY_LEVEL_DEFAULT,
)
from src.const.types import (
    AnyCallable,
    OptionalCoreCommandArgsDict,
    StringsDict,
    StringsList,
)
from src.core.command.ScriptCommand import ScriptCommand
from src.core.KernelChild import KernelChild
from src.helper.string import string_count_lines_needed, string_format_ignore_missing

if TYPE_CHECKING:
    from src.core.Kernel import Kernel

IO_DEFAULT_LOG_LENGTH = 10


class IOManagerLogMessage(TypedDict):
    message: str
    lines: int


class IOManager(KernelChild):
    def __init__(self, kernel: "Kernel") -> None:
        super().__init__(kernel)
        self.log_indent: int = 0
        self.log_length: int = IO_DEFAULT_LOG_LENGTH
        self.log_messages: List[IOManagerLogMessage] = []
        self.indent_string: str = "  "

    def error(
        self,
        message: str,
        parameters: Optional[StringsDict] = None,
        fatal: bool = True,
        trace: bool = True,
    ) -> NoReturn:
        # Performance optimisation
        import logging

        message = f"[ERROR] {string_format_ignore_missing(message, parameters)}"
        message = f"{COLOR_RED}{message}{COLOR_RESET}"

        # Support errors before logger loading
        if self.kernel.logger:
            self.kernel.logger.append_error(
                "ERROR", parameters or {}, logging.FATAL if fatal else logging.ERROR
            )

        if trace or not self.kernel.tty:
            from src.core.FatalError import FatalError

            raise FatalError(message)
            # Do not exit, allowing unit testing to catch error.
        else:
            self.print(message)
            sys.exit(0)

    def log_indent_up(self) -> None:
        self.log_indent += 1

    def log_indent_down(self) -> None:
        self.log_indent -= 1

    def build_indent(self, increment: int = 0) -> str:
        return self.indent_string * (self.log_indent + increment)

    def calc_log_messages_length(self) -> int:
        return sum(message["lines"] for message in self.log_messages)

    def log_hide(self) -> None:
        if self.log_length:
            total_lines_needed = self.calc_log_messages_length()
            self.clear_last_n_lines(total_lines_needed)

    def clear_last_n_lines(self, n: int) -> None:
        for _ in range(n):
            sys.stdout.write("\x1b[1A")  # Move cursor up by 1 line
            sys.stdout.write("\x1b[2K")  # Clear current line

    def log_show(self) -> None:
        for message in self.log_messages:
            self.print(message["message"])

    def log(
        self,
        message: Any,
        color: str = COLOR_GRAY,
        increment: int = 0,
        verbosity: int = VERBOSITY_LEVEL_DEFAULT,
    ) -> None:
        if verbosity > self.kernel.verbosity:
            return

        self.log_hide()

        message = f"{self.build_indent(increment)}{color}{message}{COLOR_RESET}"

        if self.log_length:
            # Calculate the number of lines needed for the message
            lines_needed = string_count_lines_needed(message)

            # Save the message along with its line count
            self.log_messages.append({"message": message, "lines": lines_needed})

            # Remove the oldest message if the log exceeds the frame height
            if len(self.log_messages) > self.log_length:
                self.log_messages.pop(0)

            self.log_show()
        else:
            self.print(message)

    def success(self, message: str) -> None:
        def _success() -> None:
            nonlocal message
            self.log(f"{COLOR_GREEN}✔{COLOR_RESET} {message}")

        self.exec_outside_log_frame(_success)

    def fail(self, message: str) -> None:
        def _fail() -> None:
            nonlocal message
            self.log(f"{COLOR_RED}×{COLOR_RESET} {message}")
            self.print(message)

        self.exec_outside_log_frame(_fail)

    def print(self, message: Any) -> None:
        print(message)

    def message(self, message: str, text: None | str = None) -> None:
        import textwrap

        def _message() -> None:
            nonlocal message
            nonlocal text
            message = f"{COLOR_CYAN}[wex]{COLOR_RESET} {message}"

            if text:
                message += f"{os.linesep}{COLOR_GRAY}{textwrap.indent(text, (self.log_indent + 1) * self.indent_string)}{os.linesep}"

            self.print(message)

        self.exec_outside_log_frame(_message)

    def exec_outside_log_frame(self, callback: AnyCallable) -> None:
        self.log_hide()

        callback()

        self.log_show()

    def message_next_command(
        self,
        script_command: ScriptCommand,
        args: OptionalCoreCommandArgsDict = None,
        command_type: str = COMMAND_TYPE_ADDON,
        message: str = "You might want now to execute",
    ) -> None:
        command_string = self.kernel.get_command_resolver(
            command_type
        ).build_full_command_from_function(
            script_command,
            args,
        )
        if command_string:
            self.message_all_next_commands(
                [command_string],
                command_type,
                message,
            )

    def message_all_next_commands(
        self,
        script_command_or_strings: List[ScriptCommand | str],
        command_type: str = COMMAND_TYPE_ADDON,
        message: str = "You might want now to execute one of the following command",
    ) -> None:
        commands_strings: StringsList = []
        for command in script_command_or_strings:
            if isinstance(command, ScriptCommand):
                command_string = self.kernel.get_command_resolver(
                    command_type
                ).build_full_command_from_function(
                    command,
                    {},
                )

                # Only supports commands without args
                commands_strings.append(f"{COLOR_CYAN}>{COLOR_RESET} {command_string}")
            else:
                commands_strings.append(command)

        self.message(message + ":", os.linesep.join(commands_strings))
