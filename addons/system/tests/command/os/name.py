from addons.system.command.os.name import system__os__name
from tests.AbstractTestCase import AbstractTestCase


class TestSystemCommandOsName(AbstractTestCase):
    def test_name(self):
        self.assertEqual(
            self.kernel.run_function(system__os__name, {
                'name': 'test'
            }),
            'linux'
        )
