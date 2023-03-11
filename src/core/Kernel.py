import click
import time


class Kernel:
    @click.command()
    @click.argument('command', type=str)
    def command(command, first_arg, second_arg):
        click.echo(click.style('command : ' + command, fg='cyan', bold=True))

        num_items = 1000
        with click.progressbar(range(num_items), fill_char="■", color=True) as bar:
            for i in bar:
                time.sleep(0.01)

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
