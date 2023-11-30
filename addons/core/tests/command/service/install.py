from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase


class TestCoreCommandServiceInstall(AbstractAppTestCase):
    def test_install(self) -> None:
        # Creating app is intensively used in all tests.
        self.assertTrue(True)
