from tests.AbstractTestCase import AbstractTestCase

from addons.app.helpers.test import create_test_app


class TestAppCommandAppInit(AbstractTestCase):
    def test_init(self):
        create_test_app(self.kernel, services=['php_8'])
