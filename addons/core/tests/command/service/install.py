from tests.AbstractTestCase import AbstractTestCase

from addons.app.helpers.test import create_test_app


class TestCoreCommandServiceInstall(AbstractTestCase):
    def test_install(self):
        create_test_app(self.kernel, services=['php_8'])
