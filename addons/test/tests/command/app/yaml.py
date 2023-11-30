from addons.app.command.app.exec import app__app__exec
from addons.app.tests.AbstractWebhookTestCase import AbstractWebhookTestCase
from src.core.FatalError import FatalError


class TestTestCommandAppYaml(AbstractWebhookTestCase):
    def test_yaml(self) -> None:
        with self.assertRaises(FatalError):
            self.kernel.run_command(
                "test::app/yaml",
                {
                    "option": "test",
                },
            )

        app_dir, app_name = self.create_and_start_test_app_webhook()

        self.kernel.run_function(
            app__app__exec,
            {"command": "echo TEST_VAR > /test-file", "app_dir": app_dir},
        )

        self.kernel.run_function(
            app__app__exec,
            {
                "command": 'echo "echo TEST_SCRIPT_FILE" > /test-file.sh',
                "app_dir": app_dir,
            },
        )

        self.kernel.run_function(
            app__app__exec,
            {
                "command": "echo \"print('TEST_PYTHON_FILE')\" > /test-python.py",
                "app_dir": app_dir,
            },
        )

        response = self.kernel.run_command(
            "test::app/yaml", {"option": "test", "app_dir": app_dir}
        )

        self.assertEqual(response.output_bag[0].print(), "Inline bash script example")

        self.assertResponseOutputBagItemContains(response, 1, app_dir)

        self.assertResponseOutputBagItemContains(response, 2, "TEST_VAR")

        self.assertResponseOutputBagItemContains(response, 3, "TEST_SCRIPT_FILE")

        self.assertResponseOutputBagItemContains(response, 4, "PYTHON_SUCCESS")

        self.assertResponseOutputBagItemContains(response, 5, "PYTHON_SUCCESS_FROM_FILE")

        self.assertResponseOutputBagItemContains(response, 6, "IN_CONTAINER_PYTHON_SCRIPT")

        self.assertResponseOutputBagItemContains(response, 7, "TEST_PYTHON_FILE")
