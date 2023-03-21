
from addons.core.command.registry.build import core_registry_build
from src.core.action.TestCoreAction import TestCoreAction

from src.helper.file import create_from_template


class TestCreateCoreAction(TestCoreAction):
    def exec(self, command, command_args):
        kernel = self.kernel

        match = kernel.build_match_or_fail(command)

        test_path = kernel.build_command_path_from_match(match, 'tests')
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
            core_registry_build
        )

        kernel.log_notice(f'Created test file : {test_path}')

        return test_path
