#!/usr/bin/env python3
import click
import sys
from src.core.Kernel import Kernel
import importlib


@click.group()
def cli():
    pass


if __name__ == '__main__':
    kernel = Kernel()

    if kernel.validate_argv(sys.argv):
        command = sys.argv[1]
        kernel.validate_command(command)

        module_name = 'addons.core.registry.build'
        command_name = 'core::registry/build'
        function_name = 'core_registry_build'

        module = importlib.import_module(module_name)
        function = getattr(module, function_name)

        cli.add_command(
            function,
            name=command_name
        )

        cli()
