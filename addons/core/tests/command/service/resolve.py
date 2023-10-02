from addons.core.command.service.resolve import core__service__resolve
from tests.AbstractTestCase import AbstractTestCase


class TestCoreCommandServiceResolve(AbstractTestCase):
    def test_resolve(self):
        dependencies = self.kernel.run_function(
            core__service__resolve,
            {
                'service': 'php-8, matomo'
            }).first()

        self.assertGreaterEqual(
            len(dependencies),
            2
        )
