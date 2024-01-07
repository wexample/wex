from addons.app.command.env.set import app__env__set
from addons.app.command.env.get import app__env__get
from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase


class TestAppCommandEnvSet(AbstractAppTestCase):
    def test_set(self) -> None:
        app_dir = self.create_test_app()

        self.kernel.run_function(app__env__set, {
            'app_dir': app_dir,
            "environment": "test-env"
        })

        response = self.kernel.run_function(app__env__get, {
            'app_dir': app_dir,
        })

        self.assertEqual(
            response.first(),
            'test-env'
        )
