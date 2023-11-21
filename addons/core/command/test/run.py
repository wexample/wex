from addons.core.command.core.cleanup import core__core__cleanup
from src.decorator.command import command
from src.decorator.option import option
from src.decorator.alias import alias
import os
import sys
import unittest
import importlib.util
from src.decorator.as_sudo import as_sudo
from addons.app.const.app import APP_ENV_LOCAL
from src.helper.command import execute_command_tree
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@alias('test')
@as_sudo()
@command(help="Run all tests or given command test")
@option('--command', '-c', type=str, required=False, help="Single command to test")
def core__test__run(kernel: 'Kernel', command: str = None):
    # In local env, script are started manually,
    # then we remove every docker container to ensure no
    if kernel.registry['env'] == APP_ENV_LOCAL:
        execute_command_tree(kernel, [
            'docker',
            'rm',
            '-f',
            [
                'docker',
                'ps',
                '-q',
                '--filter',
                'name=test_app_'
            ],
            '|',
            'True'
        ])

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
                    (not command) or command_name == command or (
                    command.endswith('*') and command_name.startswith(command[:-1]))):
                kernel.io.log(f'Found test for command: {command_name}')

                spec = importlib.util.spec_from_file_location(f'{command_name}_test', command_data['test'])
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                suite.addTests(loader.loadTestsFromModule(module))

    result = unittest.TextTestRunner(failfast=True).run(suite)

    if not result.wasSuccessful():
        sys.exit(1)
