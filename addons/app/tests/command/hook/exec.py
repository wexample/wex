from __future__ import annotations

from addons.app.command.hook.exec import app__hook__exec
from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase


class TestAppCommandHookExec(AbstractAppTestCase):
    def test_exec(self) -> None:
        from src.const.globals import COMMAND_CHAR_APP, COMMAND_CHAR_SERVICE

        app_dir = self.create_and_start_test_app(services=["php"])

        results = self.kernel.run_function(
            app__hook__exec,
            {
                "app-dir": app_dir,
                "hook": "missing/hook",
                # "sync": True
            },
        ).first()

        self.assertEqual(results[f"{COMMAND_CHAR_SERVICE}php"].print(), None)

        self.assertEqual(results[COMMAND_CHAR_APP].print(), None)
