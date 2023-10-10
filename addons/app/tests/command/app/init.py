from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase

class TestAppCommandAppInit(AbstractAppTestCase):
    def test_init(self):
        self.create_and_start_test_app(services=['php_8'])

        self.stop_test_app()
