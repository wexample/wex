import os.path

from addons.core.command.registry.build import core__registry__build
from src.core.action.TestCoreAction import TestCoreAction

from src.helper.file import create_from_template


class TestCreateCoreAction(TestCoreAction):
    def exec(self, command, command_args):
        if not command:
            output = []

            # Create all missing tests
            for command, command_data in self.kernel.get_all_commands().items():
                output.append(self.create_test(command))

            return output
        else:
            return self.create_test(command)

    def create_test(self, command):
        kernel = self.kernel

        match = kernel.build_match_or_fail(command)
        test_path = kernel.build_command_path_from_match(match, 'tests')

        if os.path.exists(test_path):
            return test_path

        class_name = self.file_path_to_class_name(test_path)
        method_name = self.file_path_to_test_method(test_path)

        kernel.log(f'Creating test for command {command}')

        kernel.log_indent_up()
        kernel.log(f'File : {test_path}')
        kernel.log(f'Class : {class_name}')
        kernel.log(f'Function : {method_name}')
        kernel.log_indent_down()

        create_from_template(
            kernel.path['templates'] + 'test.py.tpl',
            test_path,
            {
                'class_name': class_name,
                'method_name': method_name,
                'command': command
            }
        )

        kernel.exec_function(
            core__registry__build
        )

        kernel.log_notice(f'Created test file : {test_path}')

        return test_path
