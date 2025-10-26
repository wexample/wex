from __future__ import annotations
from tests.AbstractTestCase import AbstractTestCase


class TestCoreCommandCheckHi(AbstractTestCase):
    def test_hi(self) -> None:
        from addons.core.command.check.hi import core__check__hi

        self.assertEqual(self.kernel.run_function(core__check__hi).print(), "hi!")
