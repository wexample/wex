from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase


class TestAppCommandAppGo(AbstractAppTestCase):

    def test_go(self):
        app_dir = self.create_and_start_test_app(services=['php'])

        # We don't test app__app__go as it is an interactive command.

        self.stop_test_app()
