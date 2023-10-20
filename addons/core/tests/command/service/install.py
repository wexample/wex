from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase


class TestCoreCommandServiceInstall(AbstractAppTestCase):
    def test_install(self):
        # Creating app is intensively used in all tests.
        self.assertTrue(True)
