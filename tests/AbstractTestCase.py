import os
import shutil
import unittest
import inspect

from src.const.globals import COLOR_LIGHT_MAGENTA
from src.core.TestKernel import TestKernel
from src.helper.file import create_directories_and_copy


class AbstractTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.kernel = TestKernel(os.getcwd() + '/__main__.py')

    def setUp(self):
        # Add a new line between each test
        self.kernel.io.print("")

        self.test_dir = os.getcwd()

    def tearDown(self):
        # Add a new line between each test
        self.kernel.io.print("")

        # If workdir changed.
        current_dir = os.getcwd()
        if current_dir != self.test_dir:
            self.log(f'Reset working directory to : {self.test_dir}')

            os.chdir(self.test_dir)

    def assertPathExists(self, file_path, exists=True):
        """
        Assert that the specified file exists.
        """
        self.assertEqual(
            os.path.exists(file_path),
            exists,
            f'No such file or directory : {file_path}'
        )

    def assertDictKeysEquals(self, result, expected):
        for key, value in expected.items():
            self.assertEqual(result.get(key), value, f"Failed for key: {key}")

    def build_test_dir(self, source_dir: str) -> str:
        # English comments as requested
        # Get the directory name from source directory
        dir_name = os.path.basename(source_dir)

        # Build the destination directory path
        dest_dir = os.path.join(self.kernel.path['tmp'], 'tests', dir_name)

        # Delete the destination directory if it exists
        if os.path.exists(dest_dir):
            shutil.rmtree(dest_dir)

        # Copy everything from source directory to destination directory
        shutil.copytree(source_dir, dest_dir)

        return dest_dir

    def build_test_file(self, file_name: str) -> str:
        src_file = os.path.join(self.kernel.path['root'], 'tests', 'samples', file_name)
        dst_file = os.path.join(self.kernel.path['tmp'], 'tests', file_name)

        create_directories_and_copy(src_file, dst_file)

        return dst_file

    def write_test_result(self, name: str, data: str):
        result_path = os.path.join(self.kernel.path['tmp'], 'tests', 'results')
        os.makedirs(
            result_path,
            exist_ok=True)

        with open(f'{result_path}/{name}.txt', 'w') as file_a:
            file_a.write(data)

    def log(self, message: str):
        message = f'\n{message}' if message.count('\n') > 0 else message

        self.kernel.io.log(
            f'test[{inspect.currentframe().f_code.co_name}]:' + str(message),
            color=COLOR_LIGHT_MAGENTA
        )
