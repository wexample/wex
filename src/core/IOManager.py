import json
import os

from src.const.globals import \
    COLOR_RESET, COLOR_GRAY, COLOR_CYAN, COMMAND_TYPE_ADDON, VERBOSITY_LEVEL_DEFAULT, COLOR_GREEN, COLOR_RED


class IOManager:
    messages = None

    def __init__(self, kernel):
        self.log_indent: int = 1
        self.indent_string = '  '
        self.kernel = kernel

    def trans(self, key: str, parameters: object = {}, default=None) -> str:
        # Performance optimisation
        from src.helper.string import format_ignore_missing

        # Load the messages from the JSON file
        if self.messages is None:
            with open(self.kernel.path['root'] + 'locale/messages.json') as f:
                self.messages = json.load(f)

                for addon in self.kernel.addons:
                    messages_path = self.kernel.path['addons'] + f'{addon}/locale/messages.json'

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

    def log(self, message: str, color=COLOR_GRAY, increment: int = 0, verbosity: int = VERBOSITY_LEVEL_DEFAULT) -> None:
        if verbosity > self.kernel.verbosity:
            return

        self.print(f'{self.build_indent(increment)}{color}{message}{COLOR_RESET}')

    def success(self, message):
        self.log(f'{COLOR_GREEN}✔{COLOR_RESET} {message}')

    def fail(self, message):
        self.log(f'{COLOR_RED}×{COLOR_RESET} {message}')

    def print(self, message):
        print(message)

    def message(self, message: str, text: None | str = None):
        import textwrap

        message = f'{COLOR_CYAN}[wex]{COLOR_RESET} {message}'

        if text:
            message += f'\n{COLOR_GRAY}{textwrap.indent(text, (self.log_indent + 1) * self.indent_string)}\n'

        self.print(message)

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
        self.message(message + ':')

        commands = []
        for command in functions_or_command:
            if not isinstance(command, str):
                # Only supports commands without args
                commands.append(
                    self.kernel.get_command_resolver(command_type).build_full_command_from_function(
                        command,
                        {},
                    )
                )

        commands = '\n'.join(commands)
        self.print(
            f'{self.build_indent(2)}{COLOR_GRAY}>{COLOR_RESET} {commands}\n'
        )
