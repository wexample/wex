from addons.test.command.command.has_attached import \
    test__command__has_attached
from tests.AbstractTestCase import AbstractTestCase


class TestTestCommandCommandHasAttached(AbstractTestCase):
    def test_has_attached(self) -> None:
        response = self.kernel.run_function(test__command__has_attached, {})

        self.assertEqual(response.first(), "OK")
