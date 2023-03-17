import os
import unittest
import importlib

from addons.core.command.registry.build import core_registry_build
from src.core.action.AbstractCoreAction import AbstractCoreAction


class TestCoreAction(AbstractCoreAction):
    def exec(self, command, command_args):
        self.kernel.exec_function(
            core_registry_build
        )

        self.kernel.log('Starting test suite..')

        loader = unittest.TestLoader()
        suite = loader.discover(self.kernel.path['root'] + 'tests/')

        os.chdir(self.kernel.path['root'])

        self.kernel.log('Starting addons tests suites..')
        for addon, addon_data in self.kernel.registry['addons'].items():
            for command, command_data in addon_data['commands'].items():
                if 'test' in command_data and command_data['test']:
                    spec = importlib.util.spec_from_file_location(command + '_test', command_data['test'])
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    suite.addTests(unittest.TestLoader().loadTestsFromModule(module))

        unittest.TextTestRunner().run(suite)

    def file_path_to_class_name(self, file_path: str) -> str:
        """
        Convert a file path to a test class name.

        Example: "addon/tests/command/group/name.py" becomes "TestAddonGroupName"
        """
        file_path = os.path.relpath(file_path, self.kernel.path['addons'])
        parts = file_path.split('/')
        parts = [p.capitalize() for p in parts]
        del parts[1]
        parts[-1] = f"{parts[-1][:-3]}"
        class_name = ''.join(parts)
        return f'Test{class_name}'

    def file_path_to_test_method(self, file_path: str) -> str:
        """
        Convert a file path to a test method name.

        Example: "addon/tests/command/group/name.py"  becomes "test_name"
        """
        file_path = os.path.relpath(file_path, self.kernel.path['addons'])
        parts = file_path.split('/')
        file_name = parts[-1][:-3]
        test_method = f'test_{file_name}'
        return test_method
