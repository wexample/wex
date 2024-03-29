from addons.app.command.domain.list import app__domain__list
from addons.app.const.app import APP_DIR_APP_DATA_NAME
from addons.app.helper.test import DEFAULT_APP_TEST_NAME
from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase


class TestAppCommandDomainList(AbstractAppTestCase):
    def test_list(self) -> None:
        app_dir = self.create_test_app()

        response = self.kernel.run_function(app__domain__list, {"app-dir": app_dir})

        self.assertResponseFirstContains(
            response, DEFAULT_APP_TEST_NAME + APP_DIR_APP_DATA_NAME
        )
