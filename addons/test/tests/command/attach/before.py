from addons.test.command.attach.before import test__attach__before
from tests.AbstractTestCase import AbstractTestCase


class TestTestCommandAttachBefore(AbstractTestCase):
    def test_before(self) -> None:
        response = self.kernel.run_function(test__attach__before, {
        })

        self.assertEqual(
            response.first(),
            'BEFORE'
        )
