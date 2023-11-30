from addons.app.command.hosts.update import app__hosts__update
from tests.AbstractTestCase import AbstractTestCase


class TestAppCommandHostsUpdate(AbstractTestCase):
    def test_update(self) -> None:
        self.assertIsNone(self.kernel.run_function(app__hosts__update).first())
