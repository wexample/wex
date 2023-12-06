from addons.app.command.proxy.start import app__proxy__start
from addons.app.command.proxy.stop import app__proxy__stop
from src.helper.command import execute_command_sync
from tests.AbstractTestCase import AbstractTestCase


class TestAppCommandProxyStart(AbstractTestCase):
    def test_start(self) -> None:
        execute_command_sync(self.kernel, ["docker", "ps"])

        self.kernel.run_function(app__proxy__start)
        self.kernel.run_function(app__proxy__stop)
