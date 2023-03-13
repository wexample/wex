#!/usr/bin/env python3
import click
import sys
from src.core.Kernel import Kernel

kernel = Kernel()


@click.command()
@click.option('--myarg', type=str)
@click.option('-d', is_flag=True, type=bool)
@click.option('-f', is_flag=True, type=bool)
def first_command(myarg, d, f):
    print('EXEC')
    print(myarg)
    print(d)
    print(f)


@click.group()
def cli():
    pass


if __name__ == '__main__':
    if kernel.validate_argv(sys.argv):
        command = sys.argv[1]
        kernel.validate_command(command)

        # TODO Remove command name
        # TODO convert command to commandName
        # TODO load file and execute

        cli.add_command(
            first_command,
            name='toto::tata/truc'
        )

        cli()
