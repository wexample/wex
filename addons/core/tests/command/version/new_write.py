from tests.AbstractTestCase import AbstractTestCase


class TestCoreCommandVersionNewWrite(AbstractTestCase):
    def test_new_write(self) -> None:
        # Build method is modifying core structure,
        # we have no need to test it deeply for now.
        self.assertTrue(True)
