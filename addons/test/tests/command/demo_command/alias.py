from tests.AbstractTestCase import AbstractTestCase


class TestTestCommandDemoCommandAlias(AbstractTestCase):
    def test_alias(self) -> None:
        alias = self.kernel.run_command("this-is-a-test-alias").first()

        self.assertEqual(alias, "ALIAS")
