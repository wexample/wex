from addons.test.command.return_type.int import test__return_type__int
from tests.AbstractTestCase import AbstractTestCase


class TestTestCommandReturnTypeInt(AbstractTestCase):
    def test_int(self):
        response = self.kernel.run_function(test__return_type__int, {
            'arg': 10
        })

        self.assertEqual(
            response.first(),
            11
        )
