import inspect
import os
import shutil
import unittest

from src.const.globals import COLOR_LIGHT_MAGENTA
from src.core.TestKernel import TestKernel
from src.helper.command import execute_command_sync
from src.helper.file import file_create_directories_and_copy


class AbstractTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.kernel = TestKernel(os.getcwd() + "/__main__.py")

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
            self.log(f"Reset working directory to : {self.test_dir}")

            os.chdir(self.test_dir)

    def assertPathExists(self, file_path, exists=True):
        """
        Assert that the specified file exists.
        """
        self.assertEqual(
            os.path.exists(file_path),
            exists,
            f"No such file or directory : {file_path}",
        )

    def assertDictKeysEquals(self, result, expected):
        for key, value in expected.items():
            self.assertEqual(result.get(key), value, f"Failed for key: {key}")

    def build_test_dir(self, source_dir: str) -> str:
        # Get the directory name from source directory
        dir_name = os.path.basename(source_dir)
        tmp_dir = self.kernel.get_or_create_path("tmp")

        # Build the destination directory path
        dest_dir = os.path.join(tmp_dir, "tests", dir_name)

        # Delete the destination directory if it exists
        if os.path.exists(dest_dir):
            shutil.rmtree(dest_dir)

        # Copy everything from source directory to destination directory
        shutil.copytree(source_dir, dest_dir)

        return dest_dir

    def build_test_file(self, file_name: str) -> str:
        src_file = os.path.join(
            self.kernel.get_path("root"), "tests", "samples", file_name
        )
        dst_file = os.path.join(
            self.kernel.get_or_create_path("tmp"), "tests", file_name
        )

        file_create_directories_and_copy(src_file, dst_file)

        return dst_file

    def write_test_result(self, name: str, data: str):
        result_path = os.path.join(
            self.kernel.get_or_create_path("tmp"), "tests", "results"
        )
        os.makedirs(result_path, exist_ok=True)

        with open(f"{result_path}/{name}.txt", "w") as file_a:
            file_a.write(data)

    def log(self, message: str):
        message = str(message)
        message = (
            f"{os.linesep}{message}" if message.count(os.linesep) > 0 else f" {message}"
        )

        self.kernel.io.log(
            f"test[{inspect.currentframe().f_code.co_name}]:" + str(message),
            color=COLOR_LIGHT_MAGENTA,
        )

    def start_docker_container(self, name: str = "test_container"):
        return execute_command_sync(
            self.kernel,
            [
                "docker",
                "run",
                "-d",
                "--name",
                name,
                "debian:latest",
                "tail",
                "-f",
                "/dev/null",
            ],
        )

    def remove_docker_container(self, name: str = "test_container"):
        success, content = execute_command_sync(
            self.kernel,
            [
                "docker",
                "stop",
                name,
            ],
        )

        if not success:
            return success, content

        return execute_command_sync(
            self.kernel,
            [
                "docker",
                "rm",
                name,
            ],
        )

    def for_each_render_mode(self, callback, expected: dict):
        from src.const.globals import KERNEL_RENDER_MODES

        for render_mode in KERNEL_RENDER_MODES:
            self.log(f"Test in render mode : {render_mode}")
            value = callback(render_mode)

            if render_mode in expected:
                self.assertEqual(value, expected[render_mode], render_mode)
