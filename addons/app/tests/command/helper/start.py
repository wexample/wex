import os
import shutil

from addons.app.command.helper.start import app__helper__start
from addons.app.command.helper.stop import app__helper__stop
from addons.app.const.app import HELPER_APPS_LIST
from addons.app.helper.docker import docker_remove_filtered_container
from src.const.globals import SYSTEM_WWW_PATH
from src.helper.command import execute_command_tree_sync
from tests.AbstractTestCase import AbstractTestCase


class TestAppCommandHelperStart(AbstractTestCase):
    def test_start(self) -> None:
        for name in HELPER_APPS_LIST:
            self._test_helper_app(name)

    def _cleanup(self) -> None:
        os.chdir(self.test_dir)
        # Cleanup
        shutil.rmtree(f"{SYSTEM_WWW_PATH}test_env_one", ignore_errors=True)
        shutil.rmtree(f"{SYSTEM_WWW_PATH}test_env_two", ignore_errors=True)

    def _test_helper_app(self, name: str) -> None:
        filter = f"wex_{name}_test_env_"
        docker_remove_filtered_container(self.kernel, filter)
        self._cleanup()

        self.kernel.run_function(
            app__helper__start,
            {
                "name": name,
                "env": "test_env_one",
                "port": 8070,
                "port-secure": 44370,
            },
        )

        self.kernel.run_function(
            app__helper__start,
            {
                "name": name,
                "env": "test_env_two",
                "port": 8071,
                "port-secure": 44371,
                # Network should already exist
                "network": False,
            },
        )

        success, containers_list = execute_command_tree_sync(
            self.kernel,
            ["docker", "ps", "-q", "--filter", f"name={filter}"],
            ignore_error=True,
        )

        self.assertTrue(success)

        self.assertEqual(len(containers_list), 2)

        self.kernel.run_function(
            app__helper__stop, {"name": name, "env": "test_env_one"}
        )

        self.kernel.run_function(
            app__helper__stop, {"name": name, "env": "test_env_two"}
        )

        success, containers_list = execute_command_tree_sync(
            self.kernel,
            ["docker", "ps", "-q", "--filter", f"name={filter}"],
            ignore_error=True,
        )

        self.assertEqual(len(containers_list), 0)

        self._cleanup()
