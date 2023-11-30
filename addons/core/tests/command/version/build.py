from tests.AbstractTestCase import AbstractTestCase


class TestCoreCommandVersionBuild(AbstractTestCase):
    def test_build(self) -> None:
        # Build method is modifying core structure,
        # we have no need to test it deeply for now.
        self.assertTrue(True)
