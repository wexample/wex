#!/usr/bin/env python3

import click
from src.core.Kernel import Kernel

kernel = Kernel()


@click.command()
@click.argument('command', type=str, callback=kernel.command_validate)
def main(command):
    # options = [
    #     {'name': '--first-arg', 'short': '-f', 'type': str, 'help': 'Your first arg'},
    #     {'name': '--second-arg', 'short': '-s', 'type': str, 'help': 'Your second arg'},
    # ]
    #
    # for option in options:
    #     name = option['name']
    #     type_ = option['type']
    #     help_ = option['help']
    #     short = option['short']
    #     click.option(
    #         name,
    #         short,
    #         type=type_,
    #         help=help_,
    #     )(self.command)

    click.echo(click.style('command : ' + command, fg='cyan', bold=True))


if __name__ == '__main__':
    main()
