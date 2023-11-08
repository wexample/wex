from addons.core.command.core.cleanup import core__core__cleanup
from src.decorator.command import command
from src.decorator.option import option
from src.decorator.alias import alias
from src.core import Kernel
import os
import sys
import unittest
import importlib.util
from src.decorator.as_sudo import as_sudo


@command(help="Run all tests or given command test")
@alias('test')
@as_sudo()
@option('--command', '-c', type=str, required=False, help="Single command to test")
def core__test__run(kernel: Kernel, command: str = None):
    # Remove all temp files.
    kernel.run_function(
        function=core__core__cleanup,
        args={
            'test': True
        }
    )

    kernel.io.log('Starting test suite..')

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    os.chdir(kernel.get_path('root'))

    if not command:
        suite.addTests(
            loader.discover(
                os.path.join(kernel.get_path('root'), 'tests')
            )
        )

    kernel.io.log('Starting addons tests suites..')
    for addon_data in kernel.registry['addon'].values():
        for command_name, command_data in addon_data['commands'].items():
            if 'test' in command_data and command_data['test'] and (
                    (not command) or command_name == command):
                kernel.io.log(f'Found test for command: {command_name}')

                spec = importlib.util.spec_from_file_location(f'{command_name}_test', command_data['test'])
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                suite.addTests(loader.loadTestsFromModule(module))

    result = unittest.TextTestRunner(failfast=True).run(suite)

    if not result.wasSuccessful():
        sys.exit(1)
