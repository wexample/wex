from addons.default.command.config.get import default__config__get
from addons.default.command.config.set import default__config__set
from tests.AbstractTestCase import AbstractTestCase


class TestDefaultCommandConfigSet(AbstractTestCase):
    def test_set(self) -> None:
        file = self.build_test_file("config_bash")

        original_value = self.kernel.run_function(
            default__config__get, {"file": file, "key": "DOLOR"}
        ).print()

        # Change value.
        self.kernel.run_function(
            default__config__set,
            {
                "file": file,
                "key": "DOLOR",
                "value": "Test value",
            },
        )

        self.assertEqual(
            self.kernel.run_function(
                default__config__get, {"file": file, "key": "DOLOR"}
            ).print(),
            "Test value",
        )

        # Rollback.
        self.kernel.run_function(
            default__config__set,
            {
                "file": file,
                "key": "DOLOR",
                "value": original_value,
            },
        )

        self.assertEqual(
            self.kernel.run_function(
                default__config__get, {"file": file, "key": "DOLOR"}
            ).print(),
            original_value,
        )
