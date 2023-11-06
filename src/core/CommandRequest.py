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
        self.parent = self.resolver.kernel.current_request

        if not self.function:
            # Do not return any error if function is missing,
            # as it is managed outside.
            return

        if isinstance(args, dict):
            self.args = convert_dict_to_args(self.function, args)
        else:
            self.args = args

        # Build log
        log = {'command': self.command}

        if len(self.args):
            log['args'] = self.args

        self.log = log

    def get_root_parent(self):
        if self.parent:
            return self.parent.get_root_parent()
        return self

    def is_click_command(self, click_command) -> bool:
        return self.function.callback.__wrapped__.__code__ == click_command.callback.__wrapped__.__code__
