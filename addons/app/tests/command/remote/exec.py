from addons.app.command.remote.exec import app__remote__exec
from addons.app.helper.test import DEFAULT_ENVIRONMENT_TEST_REMOTE
from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase


class TestAppCommandRemoteExec(AbstractAppTestCase):
    def test_exec(self) -> None:
        manager = self.create_and_start_test_app_with_remote(services=["php"])
        app_dir = manager.get_app_dir()

        self.kernel.run_function(
            app__remote__exec,
            {
                "app-dir": app_dir,
                "environment": DEFAULT_ENVIRONMENT_TEST_REMOTE,
                "command": "echo TEST_ONE > /var/test-one.txt"
            }
        )

        response = self.kernel.run_function(
            app__remote__exec,
            {
                "app-dir": app_dir,
                "environment": DEFAULT_ENVIRONMENT_TEST_REMOTE,
                "command": "cat /var/test-one.txt"
            }
        )

        self.assertEqual(
            response.print_wrapped_str(),
        "TEST_ONE"
        )

        self.kernel.run_function(
            app__remote__exec,
            {
                "app-dir": app_dir,
                "environment": DEFAULT_ENVIRONMENT_TEST_REMOTE,
                "command": [
                    "echo",
                    "TEST_TWO",
                    ">",
                    "/var/test-two.txt"
                ]
            }
        )

        response = self.kernel.run_function(
            app__remote__exec,
            {
                "app-dir": app_dir,
                "environment": DEFAULT_ENVIRONMENT_TEST_REMOTE,
                "command": "cat /var/test-two.txt"
            }
        )

        self.assertEqual(
            response.print_wrapped_str(),
        "TEST_TWO"
        )
