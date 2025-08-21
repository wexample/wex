from addons.system.command.git.rollback_permissions import \
    system__git__rollback_permissions
from tests.AbstractTestCase import AbstractTestCase


class TestSystemCommandGitRollbackPermissions(AbstractTestCase):
    def test_rollback_permissions(self) -> None:
        response = self.kernel.run_function(system__git__rollback_permissions)

        self.assertTrue(
            response.first(),
        )
