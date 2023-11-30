from addons.app.command.config.get import app__config__get
from addons.app.command.config.set import app__config__set
from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase


class TestAppCommandConfigSet(AbstractAppTestCase):
    def test_set(self) -> None:
        app_dir = self.create_test_app()

        # Change value.
        self.kernel.run_function(
            app__config__set,
            {"app-dir": app_dir, "key": "global.name", "value": "wex-test-config-set"},
        )

        self.assertEqual(
            self.kernel.run_function(
                app__config__get, {"app-dir": app_dir, "key": "global.name"}
            ).first(),
            "wex-test-config-set",
        )

        # Rollback.
        self.kernel.run_function(
            app__config__set, {"app-dir": app_dir, "key": "global.name", "value": "wex"}
        )

        self.assertEqual(
            self.kernel.run_function(
                app__config__get, {"app-dir": app_dir, "key": "global.name"}
            ).first(),
            "wex",
        )
