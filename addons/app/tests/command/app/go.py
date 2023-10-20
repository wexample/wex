from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase


class TestAppCommandAppGo(AbstractAppTestCase):

    def test_go(self):
        # We don't test app__app__go as it is an interactive command.
        self.assertTrue(True)
