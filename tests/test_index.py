from AbstractTestCase import AbstractTestCase


class TestIndex(AbstractTestCase):

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
                self.assertIsNotNone(
                    command_data['test'],
                    f'Command {command} has a test file'
                )
