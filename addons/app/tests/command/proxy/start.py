from addons.app.command.proxy.start import app__proxy__start
from addons.app.command.proxy.stop import app__proxy__stop
from addons.app.AppAddonManager import AppAddonManager
from src.helper.command import execute_command_sync
from tests.AbstractTestCase import AbstractTestCase


class TestAppCommandProxyStart(AbstractTestCase):
    def test_start(self) -> None:
        manager = self.kernel.addons["app"]
        assert isinstance(manager, AppAddonManager)

        def callback() -> None:
            success, result = execute_command_sync(
                self.kernel, ["docker", "ps"]
            )

        manager.exec_in_app_workdir(
            manager.get_proxy_path(),
            callback)

        self.kernel.run_function(app__proxy__start)
        self.kernel.run_function(app__proxy__stop)
