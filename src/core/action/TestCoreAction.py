import os
import sys
import unittest
import importlib.util

from addons.core.command.registry.build import core__registry__build
from src.core.action.AbstractCoreAction import AbstractCoreAction


class TestCoreAction(AbstractCoreAction):
    @staticmethod
    def command() -> str:
        return 'test'

    def exec(self, command, command_args):
        self.kernel.exec_function(
            core__registry__build
        )

        self.kernel.log('Starting test suite..')

        loader = unittest.TestLoader()
        suite = unittest.TestSuite()
        os.chdir(self.kernel.path['root'])

        if not command:
            suite.addTests(
                loader.discover(
                    os.path.join(self.kernel.path['root'], 'tests')
                )
            )

        self.kernel.log('Starting addons tests suites..')
        for addon_data in self.kernel.registry['addons'].values():
            for command_name, command_data in addon_data['commands'].items():
                if 'test' in command_data and command_data['test'] and (
                        (not command) or command_name.startswith(command)):
                    self.kernel.log(f'Found test for command: {command_name}')

                    spec = importlib.util.spec_from_file_location(f'{command_name}_test', command_data['test'])
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    suite.addTests(loader.loadTestsFromModule(module))

        result = unittest.TextTestRunner(failfast=True).run(suite)

        if not result.wasSuccessful():
            sys.exit(1)
