from addons.core.command.test.create import core__test__create
from tests.AbstractTestCase import AbstractTestCase


class TestCoreCommandTestCreate(AbstractTestCase):
    def test_create(self) -> None:
        test_file_path_command = f"command/lorem/ipsum.py"
        test_file_path_test = (
            f"{self.kernel.get_path('addons')}core/tests/{test_file_path_command}"
        )

        response = self.kernel.run_function(
            core__test__create, {"command": "core::lorem/ipsum"}
        )

        # Command not found, no test created.
        self.assertIsNone(response.print())

        self.assertPathExists(file_path=test_file_path_test, exists=False)

        response = self.kernel.run_function(core__test__create, {"all": True})
        tests = response.print()
        assert isinstance(tests, list)

        self.assertTrue(len(tests))
