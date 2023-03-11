#!/usr/bin/env python3

import click


@click.group()
@click.argument('command_name')
def main(command_name):
    """
    A bash scripts manager.
    """
    click.echo('Addon/group/name: ' + command_name)


options = [
    {'name': '--first-arg', 'short': '-f', 'type': str, 'help': 'Your first arg'},
    {'name': '--second-arg', 'short': '-s', 'type': str, 'help': 'Your second arg'},
]

for option in options:
    name = option['name']
    type_ = option['type']
    help_ = option['help']
    main = click.option(
        name,
        type=type_,
        help=help_
    )(main)

if __name__ == '__main__':
    main()
