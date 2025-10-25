from __future__ import annotations
from tests.AbstractTestCase import AbstractTestCase


class TestDefaultCommandFileAppendOnce(AbstractTestCase):
    def test_append_once(self) -> None:
        from addons.default.command.file.append_once import default__file__append_once

        file = self.build_test_file("config_bash")

        with open(file, newline="") as f:
            file_original = f.read()
            first_line = f.readline()

        self.kernel.run_function(
            default__file__append_once, {"file": file, "line": first_line}
        )

        with open(file, newline="") as f:
            file_modified = f.read()

        self.assertEqual(
            file_original, file_modified, "The file should not be modified"
        )

        self.kernel.run_function(
            default__file__append_once, {"file": file, "line": "NEW_LINE=yes"}
        )

        with open(file, newline="") as f:
            file_modified = f.read()

        self.assertNotEqual(file_original, file_modified, "The file should be modified")
