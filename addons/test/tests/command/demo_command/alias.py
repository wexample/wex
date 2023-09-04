from tests.AbstractTestCase import AbstractTestCase


class TestTestCommandDemoCommandAlias(AbstractTestCase):
    def test_alias(self):
        alias = self.kernel.run_command(
            'this-is-a-test-alias')

        self.assertEqual(
            alias,
            'ALIAS'
        )