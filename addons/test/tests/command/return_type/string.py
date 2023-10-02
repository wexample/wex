from addons.test.command.return_type.string import test__return_type__string
from tests.AbstractTestCase import AbstractTestCase


class TestTestCommandReturnTypeString(AbstractTestCase):
    def test_string(self):
        response = self.kernel.run_function(test__return_type__string, {
            'arg': 'yes'
        })

        self.assertTrue(
            type(response.first()),
            str
        )