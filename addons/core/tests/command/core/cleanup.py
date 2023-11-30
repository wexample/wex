import os

from addons.core.command.core.cleanup import core__core__cleanup
from tests.AbstractTestCase import AbstractTestCase


class TestCoreCommandCoreCleanup(AbstractTestCase):
    def test_cleanup(self) -> None:
        result = self.kernel.run_function(
            core__core__cleanup,
        ).first()

        self.assertIsNone(
            result,
        )

        log_dir = self.kernel.get_or_create_path("task")
        log_files = os.listdir(log_dir)

        self.assertEqual(len(log_files), 0)
