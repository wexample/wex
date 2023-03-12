import click
import re


class Kernel:
    @staticmethod
    def command_validate(ctx, param, value):
        if not re.match(r"^(?:\w+::)?[\w-]+/[\w-]+$", value):
            raise click.BadParameter(
                "Invalid command format. Must be in the format 'addon::group/name' or 'group/name'")
        return value

    @click.command()
    @click.argument('command', type=str, callback=command_validate)
    @click.pass_obj
    def command(self, command, first_arg, second_arg):
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

        self.command()
