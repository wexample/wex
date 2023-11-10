from src.core.FatalError import FatalError
from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase
from addons.app.command.app.exec import app__app__exec


class TestTestCommandAppYaml(AbstractAppTestCase):
    def test_yaml(self):
        with self.assertRaises(FatalError):
            self.kernel.run_command('test::app/yaml', {
                'option': 'test',
            })

        app_dir = self.create_and_start_test_app(
            services=['php']
        )

        self.kernel.run_function(
            app__app__exec,
            {
                'command': 'echo TEST_VAR > /test-file',
                'app_dir': app_dir
            }
        )

        self.kernel.run_function(
            app__app__exec,
            {
                'command': 'echo "echo TEST_SCRIPT_FILE" > /test-file.sh',
                'app_dir': app_dir
            }
        )

        self.kernel.run_function(
            app__app__exec,
            {
                'command': 'echo "print(\'TEST_PYTHON_FILE\')" > /test-python.py',
                'app_dir': app_dir
            }
        )

        response = self.kernel.run_command('test::app/yaml', {
            'option': 'test',
            'app_dir': app_dir
        })

        self.assertEqual(
            response.output_bag[0].print(),
            'Inline bash script example'
        )

        self.assertTrue(
            app_dir in response.output_bag[1].print()
        )

        self.assertEqual(
            response.output_bag[2].print(),
            'TEST_VAR'
        )

        self.assertEqual(
            response.output_bag[3].print(),
            'TEST_SCRIPT_FILE'
        )

        self.assertEqual(
            response.output_bag[4].print(),
            'IN_CONTAINER_PYTHON_SCRIPT'
        )

        self.assertEqual(
            response.output_bag[5].print(),
            'TEST_PYTHON_FILE'
        )
