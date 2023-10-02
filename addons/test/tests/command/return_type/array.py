from addons.test.command.return_type.array import test__return_type__array
from tests.AbstractTestCase import AbstractTestCase


class TestTestCommandReturnTypeArray(AbstractTestCase):
    def test_array(self):
        response = self.kernel.run_function(test__return_type__array, {
            'arg': 'yes'
        })

        self.assertTrue(
            type(response.first()),
            list
        )
