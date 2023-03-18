from AbstractTestCase import AbstractTestCase

import click


def test_index_fake_click_function():
    pass


class TestIndex(AbstractTestCase):
    def create_fake_click_function(self):
        name_option = click.Option(["--name"])
        greeting_option = click.Option(["--greeting", "-g"], is_flag=True, default=False)
        flag_option = click.Option(["--flag", "-f"], is_flag=True, default=False)

        return click.Command(
            'test_index_fake_click_function',
            params=[name_option, greeting_option, flag_option],
            callback=test_index_fake_click_function
        )

    def test_convert_args_to_dict(self):
        args = self.kernel.convert_args_to_dict(
            self.create_fake_click_function(),
            [
                '--name', 'John',
                '-f',
                '-g', True,
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
        args = self.kernel.convert_dict_to_args(
            self.create_fake_click_function(),
            {
                'name': "John",
                'g': True,
            }
        )

        self.assertEqual(
            args,
            ['--name', 'John', '-g', True]
        )

    def test_command_line_args(self):
        self.assertTrue(
            self.kernel.validate_argv([True, True]),
        )

        self.assertFalse(
            self.kernel.validate_argv([True]),
        )

    def test_tests_coverage(self):
        for addon, addon_data in self.kernel.registry['addons'].items():
            for command, command_data in addon_data['commands'].items():
                test_file_path = command_data['test']

                self.assertIsNotNone(
                    command_data['test'],
                    f'Command {command} has a test file'
                )

                if test_file_path:
                    # Import the test module
                    spec = importlib.util.spec_from_file_location('test_module', test_file_path)
                    test_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(test_module)

                    # Check that the class and method exist
                    test_class_name = self.kernel.test_manager.file_path_to_class_name(test_file_path)
                    self.assertTrue(
                        hasattr(test_module, test_class_name),
                        f'Class {test_class_name} not found in {test_file_path}'
                    )

                    test_class = getattr(test_module, test_class_name)
                    test_method_name = self.kernel.test_manager.file_path_to_test_method(test_file_path)
                    self.assertTrue(
                        hasattr(test_class, test_method_name),
                        f'Method {test_method_name} not found in {test_class_name} class in {test_file_path}'
                    )
