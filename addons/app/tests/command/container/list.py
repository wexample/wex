from addons.app.command.container.list import app__container__list
from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase


class TestAppCommandContainerList(AbstractAppTestCase):
    def test_list(self):
        app_dir = self.create_and_start_text_app(services=['php_8'])

        response = self.kernel.run_function(
            app__container__list, {
                'app-dir': app_dir
            })

        self.assertTrue(
            'test_app_prod_php_8',
            response.first()
        )
