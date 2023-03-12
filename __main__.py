#!/usr/bin/env python3
import sys

import click
from src.core.Kernel import Kernel

kernel = Kernel()


@click.command()
@click.argument('command', type=str)
@click.argument('--first-arg', type=str)
def exec(command, __first_arg):
    print('Command : ' + command)
    print('First : ' + __first_arg)


def main():
    if not kernel.validate_argv(sys.argv):
        return

    command = sys.argv[1]
    kernel.validate_command(command)

    # TODO Remove command name
    # TODO convert command to commandName
    # TODO load file and execute

    exec()


if __name__ == '__main__':
    main()
