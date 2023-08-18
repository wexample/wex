import click
import importlib

from AbstractTestCase import AbstractTestCase
from src.helper.registry import get_all_commands
from src.helper.test import file_path_to_test_class_name, file_path_to_test_method
from src.helper.args import convert_args_to_dict, convert_dict_to_args


def test_index_fake_click_function():
    pass


def create_fake_click_function():
    name_option = click.Option(['-name'])
    greeting_option = click.Option(['--greeting', '-g'], is_flag=True, default=False)
    flag_option = click.Option(['--flag', '-f'], is_flag=True, default=False)

    return click.Command(
        'test_index_fake_click_function',
        params=[name_option, greeting_option, flag_option],
        callback=test_index_fake_click_function
    )


class TestCore(AbstractTestCase):

    def test_convert_args_to_dict(self):
        args = convert_args_to_dict(
            create_fake_click_function(),
            [
                '--name', 'John',
                '--flag',
                '--greeting',
            ]
        )

        self.assertEqual(
            args,
            {
                'name': "John",
                'flag': True,
                'greeting': True,
            }
        )

    def test_convert_dict_to_args(self):
        args = convert_dict_to_args(
            create_fake_click_function(),
            {
                'name': "John",
                'greetings': True,
            }
        )

        self.assertEqual(
            args,
            ['--name', 'John', '--greetings']
        )

    def test_core_action(self):
        self.assertEqual(
            self.kernel.exec('hi'),
            'hi!'
        )

    def test_tests_coverage(self):
        for command, command_data in get_all_commands(self.kernel.registry['addons']).items():
            test_file_path = command_data['test']

            self.assertIsNotNone(
                command_data['test'],
                f'Command {command} has a test file in : {test_file_path}'
            )

            if test_file_path:
                # Import the test module
                spec = importlib.util.spec_from_file_location('test_module', test_file_path)
                test_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(test_module)

                # Check that the class and method exist
                test_class_name = file_path_to_test_class_name(self.kernel, test_file_path)
                self.assertTrue(
                    hasattr(test_module, test_class_name),
                    f'Class {test_class_name} not found in {test_file_path}'
                )

                test_class = getattr(test_module, test_class_name)
                test_method_name = file_path_to_test_method(self.kernel, test_file_path)
                self.assertTrue(
                    hasattr(test_class, test_method_name),
                    f'Method {test_method_name} not found in {test_class_name} class in {test_file_path}'
                )
