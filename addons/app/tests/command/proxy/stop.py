from addons.app.command.proxy.start import app__proxy__start
from addons.app.command.proxy.stop import app__proxy__stop
from tests.AbstractTestCase import AbstractTestCase


class TestAppCommandProxyStop(AbstractTestCase):
    def test_stop(self):
        self.kernel.exec_function(
            app__proxy__start
        )

        self.kernel.exec_function(
            app__proxy__stop
        )
