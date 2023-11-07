from addons.test.command.return_type.str import test__return_type__str
from tests.AbstractTestCase import AbstractTestCase


class TestTestCommandReturnTypeStr(AbstractTestCase):
    def test_str(self):
        response = self.kernel.run_function(test__return_type__str, {
            'arg': 'yes'
        }).first()

        self.assertTrue(
            type(response),
            str
        )