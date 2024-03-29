from addons.app.command.container.list import app__container__list
from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase


class TestAppCommandContainerList(AbstractAppTestCase):
    def test_list(self) -> None:
        app_dir = self.create_and_start_test_app(services=["php"])

        response = self.kernel.run_function(app__container__list, {"app-dir": app_dir})

        self.assertTrue("test_app_prod_php", response.first())
