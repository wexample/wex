from tests.AbstractTestCase import AbstractTestCase


class TestCoreCommandTestCleanup(AbstractTestCase):
    def test_cleanup(self) -> None:
        # Cleanup ran before every test
        self.assertTrue(True)
