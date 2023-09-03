from addons.app.command.env.get import app__env__get
from tests.AbstractTestCase import AbstractTestCase


class TestAppCommandEnvGet(AbstractTestCase):
    def test_get(self):
        env = self.kernel.run_function(
            app__env__get
        )

        self.assertTrue(
            isinstance(env, str),
            'APP_ENV is not of type str'
        )
