from addons.test.command.attach.after import test__attach__after
from tests.AbstractTestCase import AbstractTestCase


class TestTestCommandAttachAfter(AbstractTestCase):
    def test_after(self) -> None:
        response = self.kernel.run_function(test__attach__after)

        self.assertEqual(response.first(), "AFTER")
