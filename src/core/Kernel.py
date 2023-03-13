import click
import json
import os
import re
import sys
from ..const.globals import WEX_VERSION
from ..const.error import ERR_ARGUMENT_COMMAND_MALFORMED
import importlib


class Kernel:
    version = WEX_VERSION

    def __init__(self):
        # Load the messages from the JSON file
        with open(os.getcwd() + '/locale/messages.json') as f:
            self.messages = json.load(f)

    def trans(self, key):
        return self.messages[key]

    def error(self, code):
        raise click.BadParameter(
            f"[{code}] {self.trans(code)}"
        )

    def validate_argv(self, args):
        if len(args) > 1:
            return True
        return False

    def validate_command(self, value):
        if not re.match(r"^(?:\w+::)?[\w-]+/[\w-]+$", value):
            self.error(ERR_ARGUMENT_COMMAND_MALFORMED)
        return value

    def call(self, cli):
        if not self.validate_argv(sys.argv):
            return

        command = sys.argv[1]
        self.validate_command(command)

        module_name = 'addons.core.registry.build'
        command_name = 'core::registry/build'
        function_name = 'core_registry_build'

        module = importlib.import_module(module_name)
        function = getattr(module, function_name)

        cli.add_command(
            function,
            name=command_name
        )
        cli()
