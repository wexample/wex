import re
from addons.system.command.os.name import system__os__name
from tests.AbstractTestCase import AbstractTestCase


class TestSystemCommandOsName(AbstractTestCase):
    def test_name(self):
        os_name = self.kernel.run_function(system__os__name).first()

        self.assertTrue(re.match('^[a-z]+$', os_name))
