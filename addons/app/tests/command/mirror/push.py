from tests.AbstractTestCase import AbstractTestCase
from addons.app.command.remote.available import app__remote__available


class TestAppCommandMirrorPush(AbstractTestCase):
    def test_push(self) -> None:
        response = self.kernel.run_function(
            app__remote__available, {
                "environment": "missing"}
        )

        self.assertEqual(response.first(), False)
