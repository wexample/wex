from addons.test.command.return_type.list import test__return_type__list
from tests.AbstractTestCase import AbstractTestCase


class TestTestCommandReturnTypeList(AbstractTestCase):
    def test_list(self):
        response = self.kernel.run_function(test__return_type__list, {
            'arg': 'yes'
        }).first()

        self.assertTrue(
            type(response),
            list
        )
