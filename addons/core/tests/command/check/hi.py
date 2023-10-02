from addons.core.command.check.hi import core__check__hi
from tests.AbstractTestCase import AbstractTestCase


class TestCoreCommandCheckHi(AbstractTestCase):
    def test_hi(self):
        self.assertEqual(
            self.kernel.run_function(
                core__check__hi
            ).print(),
            'hi!'
        )
