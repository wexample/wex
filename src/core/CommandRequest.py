import os

from src.helper.args import arg_shift


class CommandRequest:
    function = None
    localized = None
    match = None
    path = None

    def __init__(self, resolver, command: str, args: list = None):
        args = args or []

        self.quiet = False
        self.resolver = resolver
        self.command = resolver.resolve_alias(self.resolver.kernel, command)
        self.type = resolver.get_type()
        self.storage = {}  # Useful to store data about the current command execution
        self.args: list = args

        self.locate_function()

        if not self.function:
            return

        # For multiple steps commands like response collections
        # Share unique root request steps list.
        current_request = self.resolver.kernel.current_request
        self.steps = current_request.steps if current_request else [None]

        steps = arg_shift(self.args, 'command-request-step')
        self.steps = list(map(int, str(steps).split('.'))) if steps else self.steps

    def locate_function(self):
        # Build dynamic variables
        self.match = self.resolver.build_match(self.command)

        if self.match:
            self.path = self.resolver.build_path(self)

            if self.path and os.path.isfile(self.path):
                self.function: callable = self.resolver.get_function_from_request(self)

                return True
        return False

    def is_click_command(self, click_command) -> bool:
        return self.function.callback.__wrapped__.__code__ == click_command.callback.__wrapped__.__code__
