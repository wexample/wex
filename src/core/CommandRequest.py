class CommandRequest:
    def __init__(self, resolver, command: str, args=None):
        if args is None:
            args = []

        self.quiet = False
        self.resolver = resolver
        self.command = resolver.resolve_alias(self.resolver.kernel, command)
        self.args = args
        self.args_dict = {}
        self.type = resolver.get_type()
        self.match = resolver.build_match(self.command)
        self.path = resolver.build_path(self)
        self.function: callable = None
        # Useful to store data about the current command execution.
        self.storage = {}

    def run(self):
        self.resolver.kernel.current_request = self

        return self.resolver.run_request(self)
