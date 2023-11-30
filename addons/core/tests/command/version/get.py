from addons.core.command.version.get import core__version__get
from tests.AbstractTestCase import AbstractTestCase


class TestCoreCommandVersionGet(AbstractTestCase):
    def test_get(self) -> None:
        self.assertIsNotNone(self.kernel.run_function(core__version__get))
