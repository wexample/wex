import click
import json
import os
import re
from ..const.error import ERR_ARGUMENT_COMMAND_MALFORMED


class Kernel:
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

    def command_validate(self, ctx, param, value):
        if not re.match(r"^(?:\w+::)?[\w-]+/[\w-]+$", value):
            raise self.error(ERR_ARGUMENT_COMMAND_MALFORMED)
        return value
