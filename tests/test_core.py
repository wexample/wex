import click
import importlib

from AbstractTestCase import AbstractTestCase
from addons.core.command.command.create import core__command__create
from addons.core.command.logo.show import core__logo__show
from addons.core.command.version.build import core__version__build
from addons.core.command.test.create import core__test__create
from src.helper.system import get_user_or_sudo_user
from src.core.FatalError import FatalError
from src.const.globals import COMMAND_TYPE_ADDON, OWNER_USERNAME, CORE_COMMAND_NAME, ROOT_USERNAME
from src.helper.registry import get_all_commands_from_registry_part
from src.helper.test import file_path_to_test_class_name, file_path_to_test_method
from src.helper.args import args_convert_to_dict, args_convert_dict_to_args


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
    def test_init(self):
        user = get_user_or_sudo_user()
        message = f'Tests should be ran with sudo from non sudo user'

        self.assertNotEqual(
            user,
            ROOT_USERNAME,
            '\n'.join([
                message,
                f'  To create user : sudo adduser {OWNER_USERNAME}',
                f'  To give it sudo power : sudo usermod -aG sudo {OWNER_USERNAME}',
                f'  To switch to user : sudo su {OWNER_USERNAME}',
                f'  Then run tests : sudo {CORE_COMMAND_NAME} test'
            ])
        )

    def test_help(self):
        response = self.kernel.run_function(
            core__logo__show, {
                'help': True
            }
        )

        self.assertIsNone(
            response
        )

    def test_convert_args_to_dict(self):
        args = args_convert_to_dict(
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
        args = args_convert_dict_to_args(
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

    def test_call_command_core_action(self):
        self.assertEqual(
            self.kernel.call_command('hi'),
            'hi!'
        )

    def test_call_invalid(self):
        with self.assertRaises(FatalError, msg=None):
            self.kernel.call_command('something/unexpected')

        with self.assertRaises(FatalError, msg=None):
            self.kernel.call_command('nvfjkdvnfdkjvndfkjvnfd')

        with self.assertRaises(FatalError, msg=None):
            self.kernel.call_command('*ù:-//;!,@"#^~§')

    def test_call_command_addon(self):
        self.assertIsNotNone(
            self.kernel.call_command('core::logo/show')
        )

    def test_call_command_user(self):
        self.kernel.run_function(
            core__command__create,
            {
                'command': '~test/command-call'
            }
        )

        self.assertEqual(
            self.kernel.call_command(
                '~test/command-call',
                {
                    'option': 'test'
                }),
            # No return from newly created command
            None
        )

    def test_call_command_app(self):
        self.assertEqual(
            self.kernel.call_command('.local_command/test', {
                'local-option': 'YES'
            }),
            'OK:YES'
        )

    def test_call_command_service(self):
        self.assertEqual(
            self.kernel.call_command('@test::demo-command/first'),
            'FIRST'
        )

    def test_tests_coverage(self):
        for command, command_data in get_all_commands_from_registry_part(self.kernel.registry['addon']).items():
            test_file_path = command_data['test']

            # Display nice shortcut to create missing test
            if not command_data['test']:
                self.kernel.io.message_next_command(
                    core__test__create,
                    {
                        'all': True
                    }
                )

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

    def test_build_command(self):
        self.assertEqual(
            self.kernel.get_command_resolver(COMMAND_TYPE_ADDON).build_command_from_function(
                core__logo__show),
            'core::logo/show'
        )
        self.assertEqual(
            self.kernel.get_command_resolver(COMMAND_TYPE_ADDON).build_full_command_from_function(
                core__version__build),
            'wex core::version/build'
        )

    def test_message_next_command(self):
        self.kernel.io.message_next_command(
            core__logo__show
        )
