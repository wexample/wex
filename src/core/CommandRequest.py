import os
from src.helper.args import convert_dict_to_args, convert_args_to_dict


class CommandRequest:
    function = None
    localized = None
    match = None
    path = None

    def __init__(self, resolver, command: str, args: dict | list = None):
        if args is None:
            args = []

        self.quiet = False
        self.resolver = resolver
        self.command = resolver.resolve_alias(self.resolver.kernel, command)
        self.type = resolver.get_type()
        self.storage = {}  # Useful to store data about the current command execution

        self.args_dict: dict | None = None
        self.args: dict | None = None

        if isinstance(args, dict):
            self.args_dict: dict = args
        else:
            self.args: list = args

        self.localize()

    def localize(self):
        # Build dynamic variables
        self.match = self.resolver.build_match(self.command)

        if self.match:
            self.path = self.resolver.build_path(self)

            if self.path and os.path.isfile(self.path):
                self.localized = True
                self.function: callable = self.resolver.get_function_from_request(self)

                if self.args is None:
                    self.args = convert_dict_to_args(self.function, self.args_dict)
                else:
                    self.args_dict = convert_args_to_dict(self.function, self.args)

    def run(self):
        self.resolver.kernel.current_request = self

        self.resolver.kernel.logger.append_request(self)

        return self.resolver.run_request(self)

    def is_click_command(self, click_command) -> bool:
        return self.function.callback.__wrapped__.__code__ == click_command.callback.__wrapped__.__code__
