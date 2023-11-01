import json
import os
import sys

from src.helper.string import count_lines_needed
from src.const.globals import \
    COLOR_RESET, COLOR_GRAY, COLOR_CYAN, COMMAND_TYPE_ADDON, VERBOSITY_LEVEL_DEFAULT, COLOR_GREEN, COLOR_RED

IO_DEFAULT_LOG_LENGTH = 10


class IOManager:
    messages = None

    def __init__(self, kernel):
        self.log_indent: int = 1
        self.log_length: int = IO_DEFAULT_LOG_LENGTH
        self.log_messages: list = []
        self.indent_string = '  '
        self.kernel = kernel

    def trans(self, key: str, parameters: object = {}, default=None) -> str:
        # Performance optimisation
        from src.helper.string import format_ignore_missing

        # Load the messages from the JSON file
        if self.messages is None:
            with open(self.kernel.get_path('root') + 'locale/messages.json') as f:
                self.messages = json.load(f)

                for addon in self.kernel.addons:
                    messages_path = self.kernel.get_path('addons') + f'{addon}/locale/messages.json'

                    if os.path.exists(messages_path):
                        with open(messages_path) as file:
                            self.messages.update(json.load(file))

        return format_ignore_missing(
            self.messages.get(key, default or key),
            parameters
        )

    def error(self, code: str, parameters: None | dict = None, log_level: int | None = None) -> None:
        # Performance optimisation
        import logging
        from src.const.error import COLORS

        if log_level is None:
            log_level = logging.FATAL

        message = f'[{code}] {self.trans(code, parameters, "Unexpected error")}'
        message = f'{COLORS[log_level]}{message}{COLOR_RESET}'

        self.kernel.logger.append_error(
            code,
            parameters or {},
            log_level
        )

        if log_level == logging.FATAL:
            from src.core.FatalError import FatalError

            raise FatalError(message)
        else:
            self.print(message)

    def log_indent_up(self) -> None:
        self.log_indent += 1

    def log_indent_down(self) -> None:
        self.log_indent -= 1

    def build_indent(self, increment: int = 0) -> str:
        return self.indent_string * (self.log_indent + increment)

    def calc_log_messages_length(self):
        return sum(message['lines'] for message in self.log_messages)

    def log_hide(self):
        if self.log_length:
            total_lines_needed = self.calc_log_messages_length()
            self.clear_last_n_lines(total_lines_needed)

    def clear_last_n_lines(self, n):
        for _ in range(n):
            sys.stdout.write("\x1b[1A")  # Move cursor up by 1 line
            sys.stdout.write("\x1b[2K")  # Clear current line

    def log_show(self):
        for message in self.log_messages:
            self.print(message['message'])

    def log(self, message: str, color=COLOR_GRAY, increment: int = 0, verbosity: int = VERBOSITY_LEVEL_DEFAULT) -> None:
        if verbosity > self.kernel.verbosity:
            return

        self.log_hide()

        message = f'{self.build_indent(increment)}{color}{message}{COLOR_RESET}'

        if self.log_length:
            # Calculate the number of lines needed for the message
            lines_needed = count_lines_needed(message)

            # Save the message along with its line count
            self.log_messages.append({
                'message': message,
                'lines': lines_needed
            })

            # Remove the oldest message if the log exceeds the frame height
            if len(self.log_messages) > self.log_length:
                self.log_messages.pop(0)

            self.log_show()
        else:
            self.print(message)

    def success(self, message):
        def _success():
            nonlocal message
            self.log(f'{COLOR_GREEN}✔{COLOR_RESET} {message}')

        self.exec_outside_log_frame(_success)

    def fail(self, message):
        def _fail():
            nonlocal message
            self.log(f'{COLOR_RED}×{COLOR_RESET} {message}')
            self.print(message)

        self.exec_outside_log_frame(_fail)

    def print(self, message, **kwargs):
        print(message, **kwargs)

    def message(self, message: str, text: None | str = None):
        import textwrap

        def _message():
            nonlocal message
            nonlocal text
            message = f'{COLOR_CYAN}[wex]{COLOR_RESET} {message}'

            if text:
                message += f'\n{COLOR_GRAY}{textwrap.indent(text, (self.log_indent + 1) * self.indent_string)}\n'

            self.print(message)

        self.exec_outside_log_frame(_message)

    def exec_outside_log_frame(self, callback: callable):
        self.log_hide()

        callback()

        self.log_show()

    def message_next_command(
            self,
            function_or_command,
            args: dict | None = None,
            command_type: str = COMMAND_TYPE_ADDON,
            message: str = 'You might want now to execute'):
        return self.message_all_next_commands(
            [
                self.kernel.get_command_resolver(command_type).build_full_command_from_function(
                    function_or_command,
                    args or {},
                )
            ],
            command_type,
            message
        )

    def message_all_next_commands(
            self,
            functions_or_command,
            command_type: str = COMMAND_TYPE_ADDON,
            message: str = 'You might want now to execute one of the following command',
    ):
        commands = []
        for command in functions_or_command:
            if not isinstance(command, str):
                command_string = self.kernel.get_command_resolver(command_type).build_full_command_from_function(
                    command,
                    {},
                )

                # Only supports commands without args
                commands.append(
                    f'{COLOR_CYAN}>{COLOR_RESET} {command_string}'
                )

        commands = '\n'.join(commands)
        self.message(message + ':', commands)
