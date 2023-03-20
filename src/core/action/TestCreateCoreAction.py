import os

from addons.core.command.registry.build import core_registry_build
from src.const.error import ERR_ARGUMENT_COMMAND_MALFORMED
from src.core.action.TestCoreAction import TestCoreAction


class TestCreateCoreAction(TestCoreAction):
    def exec(self, command, command_args):
        if not command:
            self.kernel.error(ERR_ARGUMENT_COMMAND_MALFORMED)

        command_path = self.kernel.build_command_path_from_command(command, 'tests')
        class_name = self.file_path_to_class_name(command_path)
        method_name = self.file_path_to_test_method(command_path)
        template_path = self.kernel.path['root'] + 'src/resources/templates/test.py.tpl'

        self.kernel.log(f'Creating test for command {command}')

        self.kernel.log_indent_up()
        self.kernel.log(f'File : {command_path}')
        self.kernel.log(f'Class : {class_name}')
        self.kernel.log(f'Function : {method_name}')
        self.kernel.log_indent_down()

        with open(template_path, 'r') as template_file:
            template_content = template_file.read()

        formatted_content = template_content.format(
            class_name=class_name,
            function_name=method_name,
            command=command
        )

        os.makedirs(
            os.path.dirname(command_path),
            exist_ok=True
        )

        with open(command_path, 'w') as output_file:
            output_file.write(formatted_content)

        self.kernel.exec_function(
            core_registry_build
        )

        self.kernel.log_notice(f'Created test file : {command_path}')
