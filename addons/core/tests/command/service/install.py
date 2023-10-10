from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase


class TestCoreCommandServiceInstall(AbstractAppTestCase):
    def test_install(self):
        self.create_test_app()

        self.stop_test_app()
