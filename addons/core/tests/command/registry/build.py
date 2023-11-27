from addons.core.command.registry.build import core__registry__build
from tests.AbstractTestCase import AbstractTestCase


class TestCoreCommandRegistryBuild(AbstractTestCase):
    def test_build(self):
        registry = self.kernel.run_function(
            core__registry__build, {"write": False}
        ).first()

        self.assertIsInstance(registry, dict)
