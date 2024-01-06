from addons.test.command.attach.after import test__attach__after
from tests.AbstractTestCase import AbstractTestCase


class TestTestCommandAttachAfter(AbstractTestCase):
    def test_after(self) -> None:
        # TODO
        response = self.kernel.run_function(test__attach__after, {
            'option': 'test'
        })

        self.assertEqual(
            response.first(),
            'something'
        )
