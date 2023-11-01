from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase
from addons.app.command.domain.list import app__domain__list
from addons.app.helpers.test import DEFAULT_APP_TEST_NAME


class TestAppCommandDomainList(AbstractAppTestCase):
    def test_list(self):
        app_dir = self.create_test_app()

        response = self.kernel.run_function(
            app__domain__list,
            {
                'app-dir': app_dir
            }
        )

        self.assertTrue(
            DEFAULT_APP_TEST_NAME + '.wex' in response.first()
        )
