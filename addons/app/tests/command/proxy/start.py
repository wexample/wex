from addons.app.command.proxy.start import app__proxy__start
from addons.app.command.proxy.stop import app__proxy__stop
from src.helper.command import execute_command_tree_sync
from tests.AbstractTestCase import AbstractTestCase
from addons.app.helper.docker import docker_remove_filtered_container


class TestAppCommandProxyStart(AbstractTestCase):
    def test_start(self) -> None:
        filter = "wex_proxy_start_test_"
        docker_remove_filtered_container(self.kernel, filter)

        self.kernel.run_function(app__proxy__start, {
            "env": "start_test_one",
            "port": 8070,
            "port-secure": 44370,
        })

        self.kernel.run_function(app__proxy__start, {
            "env": "start_test_two",
            "port": 8071,
            "port-secure": 44371,
        })

        success, prox_containers_list = execute_command_tree_sync(
            self.kernel,
            ["docker", "ps", "-q", "--filter", f"name={filter}"],
            ignore_error=True,
        )

        self.assertTrue(
            success
        )

        self.assertEqual(
            len(prox_containers_list),
            2
        )

        self.kernel.run_function(app__proxy__stop, {
            "env": "start_test_one"
        })

        self.kernel.run_function(app__proxy__stop, {
            "env": "start_test_two"
        })

        success, prox_containers_list = execute_command_tree_sync(
            self.kernel,
            ["docker", "ps", "-q", "--filter", f"name={filter}"],
            ignore_error=True,
        )

        self.assertEqual(
            len(prox_containers_list),
            0
        )
