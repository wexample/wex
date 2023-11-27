from addons.app.command.remote.available import app__remote__available
from addons.app.const.app import APP_ENV_LOCAL
from tests.AbstractTestCase import AbstractTestCase


class TestAppCommandRemoteAvailable(AbstractTestCase):
    def test_available(self):
        response = self.kernel.run_function(
            app__remote__available, {"environment": APP_ENV_LOCAL}
        )

        self.assertEqual(response.first(), False)
