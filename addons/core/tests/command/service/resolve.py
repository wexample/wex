from addons.core.command.service.resolve import core__service__resolve
from tests.AbstractTestCase import AbstractTestCase


class TestCoreCommandServiceResolve(AbstractTestCase):
    def test_resolve(self):
        dependencies = self.kernel.exec_function(
            core__service__resolve,
            {
                'service': 'php-8, matomo'
            })

        self.assertGreaterEqual(
            len(dependencies),
            2
        )
