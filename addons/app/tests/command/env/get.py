from tests.AbstractTestCase import AbstractTestCase


class TestAppCommandEnvGet(AbstractTestCase):
    def test_get(self):
        env = self.kernel.exec('app::env/get')

        self.assertTrue(
            isinstance(env, str),
            'APP_ENV is not of type str'
        )
