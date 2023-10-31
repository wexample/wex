import os

from addons.app.command.script.exec import app__script__exec
from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase
from addons.app.const.app import APP_DIR_APP_DATA
from src.helper.file import create_directories_and_copy


class TestAppCommandScriptExec(AbstractAppTestCase):
    def test_exec(self):
        app_dir = self.create_test_app(services=['php'])

        create_directories_and_copy(
            os.path.join(
                self.get_app_resources_path(),
                '5.0.0',
                APP_DIR_APP_DATA,
                'script',
                'test.yml'
            ),
            os.path.join(
                app_dir,
                APP_DIR_APP_DATA,
                'script',
                'test.yml'
            )
        )

        # Missing script
        response = self.kernel.run_function(app__script__exec, {
            'name': 'missing',
            'app-dir': app_dir
        })

        self.assertIsNone(
            response.first()
        )

        # Missing script
        response = self.kernel.run_function(app__script__exec, {
            'name': 'test',
            'app-dir': app_dir
        })

        self.assertEqual(
            response.output_bag[0].first(),
            'SIMPLE_COMMAND'
        )

        self.assertEqual(
            response.output_bag[1].first(),
            'OUTSIDE'
        )

        self.assertEqual(
            response.output_bag[2].first(),
            'INSIDE'
        )
