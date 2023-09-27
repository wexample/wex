import os
from src.helper.args import convert_dict_to_args, convert_args_to_dict


class CommandRequest:
    function = None
    localized = None
    match = None
    path = None

    def __init__(self, resolver, command: str, args: dict | list = None):
        args = args or []

        self.quiet = False
        self.resolver = resolver
        self.command = resolver.resolve_alias(self.resolver.kernel, command)
        self.type = resolver.get_type()
        self.storage = {}  # Useful to store data about the current command execution
        self.verbosity = 1
        # For multiple steps commands like response collections
        self.step = None

        self.args_dict: dict | None = None
        self.args: dict | None = None

        if isinstance(args, dict):
            self.args_dict: dict = args
        else:
            self.args: list = args

        self.locate_function()

        if self.function:
            if self.args is not None:
                self.args_dict = convert_args_to_dict(self.function, self.args)

            if 'command-request-step' in self.args_dict:
                self.step = int(self.args_dict['command-request-step'])

            if 'quiet' in self.args_dict:
                self.verbosity = 0
            elif 'vv' in self.args_dict:
                self.verbosity = 2
            elif 'vvv' in self.args_dict:
                self.verbosity = 3

            for name in [
                'command-request-step',
                'kernel-task-id',
                'quiet',
                'vv',
                'vvv',
            ]:
                if name in self.args_dict:
                    del self.args_dict[name]

            self.args = convert_dict_to_args(self.function, self.args_dict)

    def locate_function(self):
        # Build dynamic variables
        self.match = self.resolver.build_match(self.command)

        if self.match:
            self.path = self.resolver.build_path(self)

            if self.path and os.path.isfile(self.path):
                self.localized = True
                self.function: callable = self.resolver.get_function_from_request(self)

                return True
        return False

    def run(self):
        self.resolver.kernel.current_request = self

        self.resolver.kernel.logger.append_request(self)

        return self.resolver.run_request(self)

    def is_click_command(self, click_command) -> bool:
        return self.function.callback.__wrapped__.__code__ == click_command.callback.__wrapped__.__code__
