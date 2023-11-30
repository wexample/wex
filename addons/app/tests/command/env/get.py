from addons.app.command.env.get import app__env__get
from tests.AbstractTestCase import AbstractTestCase


class TestAppCommandEnvGet(AbstractTestCase):
    def test_get(self) -> None:
        env = self.kernel.run_function(app__env__get).first()

        self.assertTrue(isinstance(env, str), "APP_ENV is not of type str")
