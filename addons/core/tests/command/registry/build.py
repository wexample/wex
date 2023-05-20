import os

from tests.AbstractTestCase import AbstractTestCase
from src.const.globals import FILE_REGISTRY


class TestCoreCommandRegistryBuild(AbstractTestCase):
    def test_build(self):
        registry_path = f'{self.kernel.path["tmp"]}{FILE_REGISTRY}'

        os.remove(registry_path)
        self.kernel.exec('core::registry/build')

        self.assertFileExists(registry_path)
