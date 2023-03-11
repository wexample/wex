import click


class Kernel:
    @click.command()
    @click.argument('command', type=str)
    def command(command, first_arg, second_arg):
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
