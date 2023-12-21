from addons.app.command.version.new import app__version__new
from tests.AbstractTestCase import AbstractTestCase


class TestAppCommandVersionNew(AbstractTestCase):
    def test_new(self) -> None:
        # TODO
        response = self.kernel.run_function(app__version__new, {
            'option': 'test'
        })

        self.assertEqual(
            response.first(),
            'something'
        )
