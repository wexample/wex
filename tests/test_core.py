import click

from AbstractTestCase import AbstractTestCase
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
            ['--name', 'John', '--greetings', True]
        )

    def test_core_action(self):
        self.assertEqual(
            self.kernel.exec('hi'),
            'hi!'
        )
