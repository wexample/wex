import os

from src.helper.args import arg_shift, convert_dict_to_args


class CommandRequest:
    function = None
    localized = None
    match = None
    path = None

    def __init__(self, resolver, command: str, args: dict | list = None):
        args = args or []

        self.quiet = False
        self.resolver = resolver
        self.command = resolver.resolve_alias(command)
        self.type = resolver.get_type()
        self.storage = {}  # Useful to store data about the current command execution
        self.args = []
        self.steps = []
        self.resolver.locate_function(self)

        if not self.function:
            # Do not return any error if function is missing,
            # as it is managed outside.
            return

        if isinstance(args, dict):
            self.args = convert_dict_to_args(self.function, args)
        else:
            self.args = args

        # For multiple steps commands like response collections
        # Share a unique root request steps list.
        current_request = self.resolver.kernel.current_request
        self.steps = current_request.steps if current_request else [None]

        steps = arg_shift(self.args, 'command-request-step')
        if steps:
            self.steps = list(map(int, str(steps).split('.')))

        # Build log
        log = {'command': self.command}

        if len(self.args):
            log['args'] = self.args

        if steps:
            log['steps'] = self.steps

        self.log = log

    def is_click_command(self, click_command) -> bool:
        return self.function.callback.__wrapped__.__code__ == click_command.callback.__wrapped__.__code__
