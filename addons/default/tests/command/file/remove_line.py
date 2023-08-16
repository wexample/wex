from addons.default.command.file.remove_line import default__file__remove_line
from tests.AbstractTestCase import AbstractTestCase


class TestDefaultCommandFileRemove_line(AbstractTestCase):
    def test_remove_line(self):
        file = self.build_test_file_path('config_bash')

        with open(file, 'r', newline='') as f:
            first_line = f.readline()

        with open(file, 'r', newline='') as f:
            file_original = f.read()

        self.kernel.exec_function(
            default__file__remove_line,
            {
                'file-path': file,
                'line': first_line
            }
        )

        with open(file, 'r', newline='') as f:
            file_modified = f.read()

        self.assertNotEqual(
            file_original,
            file_modified,
            'The file should be modified'
        )
