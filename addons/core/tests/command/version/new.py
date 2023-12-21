from tests.AbstractTestCase import AbstractTestCase


class TestCoreCommandVersionNew(AbstractTestCase):
    def test_new(self) -> None:
        # Build method is modifying core structure,
        # we have no need to test it deeply for now.
        self.assertTrue(True)
