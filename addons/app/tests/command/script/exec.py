import os
import shutil

from addons.app.command.script.exec import app__script__exec
from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase
from addons.app.const.app import APP_DIR_APP_DATA
from src.core.FatalError import FatalError
from addons.app.command.app.exec import app__app__exec


class TestAppCommandScriptExec(AbstractAppTestCase):
    def copy_script_dir(self, app_dir):
        script_dir = os.path.join(
            app_dir,
            APP_DIR_APP_DATA,
            'script',
        )

        shutil.rmtree(script_dir)

        shutil.copytree(
            os.path.join(
                self.get_app_resources_path(),
                '5.0.0',
                APP_DIR_APP_DATA,
                'script',
            ),
            script_dir
        )

    def test_exec(self):
        app_dir = self.create_test_app(
            services=['php'],
            force_restart=True
        )

        self.stop_test_app(app_dir)
        self.copy_script_dir(app_dir)

        # Missing script
        response = self.kernel.run_function(app__script__exec, {
            'name': 'missing',
            'app-dir': app_dir
        })

        # self.assertIsNone(
        #     response.first()
        # )
        #
        # # Test script
        # response = self.kernel.run_function(app__script__exec, {
        #     'name': 'test',
        #     'app-dir': app_dir
        # })
        #
        # self.assertEqual(
        #     response.output_bag[0].first(),
        #     'MINIMAL_BASH_RESPONSE'
        # )
        #
        # self.assertEqual(
        #     response.output_bag[1].first(),
        #     'BASH_RESPONSE'
        # )
        #
        # self.assertEqual(
        #     response.output_bag[2].first(),
        #     'BASH_RESPONSE_FROM_FILE'
        # )
        #
        # self.assertEqual(
        #     response.output_bag[3].first(),
        #     'PYTHON_SUCCESS'
        # )
        #
        # self.assertEqual(
        #     response.output_bag[4].first(),
        #     'PYTHON_SUCCESS_FROM_FILE'
        # )

        # Inside container, should fail when app not started
        with self.assertRaises(FatalError, msg=None):
            response = self.kernel.run_function(app__script__exec, {
                'name': 'test_running',
                'app-dir': app_dir
            })

        app_dir = self.create_and_start_test_app(
            services=['php'],
            # force_restart=True
        )

        self.copy_script_dir(app_dir)

        self.kernel.run_function(app__app__exec, {
            'app-dir': app_dir,
            'command': 'touch /var/tmp/test-file'
        })

        response = self.kernel.run_function(app__script__exec, {
            'name': 'test_running',
            'app-dir': app_dir
        })

        self.assertEqual(
            response.output_bag[0].first(),
            'BASH_RESPONSE_RUNNING'
        )

        self.assertTrue(
            ' test-file' in response.output_bag[1].first()
        )

        self.assertEqual(
            response.output_bag[2].first(),
            'TEST_EXECUTION_ORDER'
        )

