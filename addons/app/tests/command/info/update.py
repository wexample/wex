from addons.app.command.info.update import app__info__update
from tests.AbstractTestCase import AbstractTestCase


class TestAppCommandInfoUpdate(AbstractTestCase):
    def test_update(self) -> None:
        response = self.kernel.run_function(app__info__update)

        self.assertTrue(isinstance(response.first(), dict))
