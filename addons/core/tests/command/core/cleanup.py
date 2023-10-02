from addons.core.command.core.cleanup import core__core__cleanup
from tests.AbstractTestCase import AbstractTestCase


class TestCoreCommandCoreCleanup(AbstractTestCase):
    def test_cleanup(self):
        result = self.kernel.run_function(
            core__core__cleanup,
        ).first()

        self.assertIsNone(
            result,
        )
