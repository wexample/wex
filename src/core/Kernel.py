import click
import re
import json
from ..const.error import ERR_ARGUMENT_COMMAND_MALFORMED
import os


class Kernel:
    def __init__(self):
        # Load the messages from the JSON file
        with open(os.getcwd() + '/locale/messages.json') as f:
            self.messages = json.load(f)

    def trans(self, key):
        return self.messages[key]

    def error(self, code):
        raise click.BadParameter(
            '[' + code + '] ' + self.trans(code)
        )

    def command_validate(self, ctx, param, value):
        if not re.match(r"^(?:\w+::)?[\w-]+/[\w-]+$", value):
            raise self.error(ERR_ARGUMENT_COMMAND_MALFORMED)
        return value

    @click.command()
    def command(self, command):
        click.echo(click.style('command : ' + command, fg='cyan', bold=True))

    def setup(self):
        options = [
            {'name': '--first-arg', 'short': '-f', 'type': str, 'help': 'Your first arg'},
            {'name': '--second-arg', 'short': '-s', 'type': str, 'help': 'Your second arg'},
        ]

        for option in options:
            name = option['name']
            type_ = option['type']
            help_ = option['help']
            short = option['short']
            click.option(
                name,
                short,
                type=type_,
                help=help_,
            )(self.command)

        # Binding validation in non-static context (keeping reference to self).
        self.command = click.argument(
            'command',
            type=str,
            callback=self.command_validate
        )(self.command)

        self.command()
