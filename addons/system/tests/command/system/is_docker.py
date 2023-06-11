from addons.system.command.system.is_docker import system__system__is_docker
from tests.AbstractTestCase import AbstractTestCase


class TestSystemCommandSystemIs_docker(AbstractTestCase):
    def test_is_docker(self):
        result = self.kernel.exec_function(
            system__system__is_docker
        )

        self.assertTrue(
            isinstance(result, bool)
        )
