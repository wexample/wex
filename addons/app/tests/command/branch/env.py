from addons.app.AppAddonManager import AppAddonManager
from addons.app.command.branch.env import app__branch__env
from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase


class TestAppCommandBranchEnv(AbstractAppTestCase):
    def test_env(self) -> None:
        app_dir = self.create_test_app(force_restart=True)
        fake_branch = "testing"
        manager = AppAddonManager(self.kernel, app_dir=app_dir)
        manager.set_config("env.test_env.branch", fake_branch)

        response = self.kernel.run_function(app__branch__env, {"branch": fake_branch})

        self.assertEqual(response.first(), "test_env")
