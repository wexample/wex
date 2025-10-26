from __future__ import annotations

from tests.AbstractTestCase import AbstractTestCase


class TestDefaultCommandFileRemoveLine(AbstractTestCase):
    def test_remove_line(self) -> None:
        from addons.default.command.file.remove_line import default__file__remove_line

        file = self.build_test_file("config_bash")

        with open(file, newline="") as f:
            first_line = f.readline()

        with open(file, newline="") as f:
            file_original = f.read()

        self.kernel.run_function(
            default__file__remove_line, {"file-path": file, "line": first_line}
        )

        with open(file, newline="") as f:
            file_modified = f.read()

        self.assertNotEqual(file_original, file_modified, "The file should be modified")
