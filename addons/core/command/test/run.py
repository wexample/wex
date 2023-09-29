from src.decorator.command import command
from src.decorator.option import option
from src.decorator.alias import alias
from src.core import Kernel
import os
import sys
import unittest
import importlib.util

from addons.core.command.registry.build import core__registry__build


@command(help="Run all tests or given command test")
@alias('test')
@option('--command', '-c', type=str, required=False, help="Single command to test")
def core__test__run(kernel: Kernel, command: str = None):
    kernel.rebuild(test=True)

    kernel.log('Starting test suite..')

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    os.chdir(kernel.path['root'])

    if not command:
        suite.addTests(
            loader.discover(
                os.path.join(kernel.path['root'], 'tests')
            )
        )

    kernel.log('Starting addons tests suites..')
    for addon_data in kernel.registry['addons'].values():
        for command_name, command_data in addon_data['commands'].items():
            if 'test' in command_data and command_data['test'] and (
                    (not command) or command_name == command):
                kernel.log(f'Found test for command: {command_name}')

                spec = importlib.util.spec_from_file_location(f'{command_name}_test', command_data['test'])
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                suite.addTests(loader.loadTestsFromModule(module))

    result = unittest.TextTestRunner(failfast=True).run(suite)

    if not result.wasSuccessful():
        sys.exit(1)
