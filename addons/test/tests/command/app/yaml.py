from src.core.FatalError import FatalError
from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase


class TestTestCommandAppYaml(AbstractAppTestCase):
    def test_yaml(self):
        with self.assertRaises(FatalError):
            self.kernel.run_command('test::app/yaml', {
                'option': 'test',
            })

        app_dir = self.create_and_start_test_app(
            services=['php'],
            force_restart=True
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

