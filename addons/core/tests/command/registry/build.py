import os

from tests.AbstractTestCase import AbstractTestCase
from src.const.globals import FILE_REGISTRY
from src.helper.file import remove_file_if_exists


class TestCoreCommandRegistryBuild(AbstractTestCase):
    def test_build(self):
        registry_path = f'{self.kernel.path["tmp"]}{FILE_REGISTRY}'

        remove_file_if_exists(registry_path)

        self.kernel.exec('core::registry/build')

        self.assertPathExists(registry_path)
