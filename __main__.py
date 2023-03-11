#!/usr/bin/env python3

import click

@click.command()
@click.argument('command_name')
@click.option('-a', '--first-arg', type=str, help='Your first arg')
def main(command_name, first_arg):
    """
    A bash scripts manager.
    """
    click.echo('Addon/group/name: ' + command_name)
    if first_arg:
        click.echo('First arg: ' + first_arg)

if __name__ == '__main__':
    main()
