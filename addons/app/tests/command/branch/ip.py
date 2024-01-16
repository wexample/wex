from addons.app.command.branch.ip import app__branch__ip
from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase
from addons.app.AppAddonManager import AppAddonManager


class TestAppCommandBranchIp(AbstractAppTestCase):
    def test_ip(self) -> None:
        app_dir = self.create_test_app(

        )
        fake_branch = "testing"
        fake_ip = "1.2.3.4"
        manager = AppAddonManager(self.kernel, app_dir=app_dir)
        manager.set_config("env.test.branch", fake_branch)
        manager.set_config("env.test.server.ip", fake_ip)

        response = self.kernel.run_function(
            app__branch__ip, {
                'branch': fake_branch
            })

        self.assertEqual(
            response.first(),
            fake_ip
        )
