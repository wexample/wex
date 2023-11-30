from addons.app.command.remote.go import app__remote__go
from addons.app.const.app import APP_ENV_TEST
from tests.AbstractTestCase import AbstractTestCase


class TestAppCommandRemoteGo(AbstractTestCase):
    def test_go(self) -> None:
        response = self.kernel.run_function(
            app__remote__go, {"environment": APP_ENV_TEST}
        )

        self.assertIsNone(response.first())
