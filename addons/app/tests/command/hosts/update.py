from addons.app.command.hosts.update import app__hosts__update
from tests.AbstractTestCase import AbstractTestCase


class TestAppCommandHostsUpdate(AbstractTestCase):
    def test_update(self):
        self.kernel.exec_function(app__hosts__update, {
            'name': 'test'
        })

        self.assertTrue(False)
