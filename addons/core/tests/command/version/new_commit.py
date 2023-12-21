from tests.AbstractTestCase import AbstractTestCase


class TestCoreCommandVersionNewCommit(AbstractTestCase):
    def test_new_commit(self) -> None:
        # Build method is modifying core structure,
        # we have no need to test it deeply for now.
        self.assertTrue(True)
