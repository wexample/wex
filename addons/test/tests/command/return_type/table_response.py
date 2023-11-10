from addons.test.command.return_type.table_response import test__return_type__table_response
from src.const.globals import KERNEL_RENDER_MODE_JSON
from tests.AbstractTestCase import AbstractTestCase


class TestTestCommandReturnTypeTableResponse(AbstractTestCase):
    def test_table_response(self):
        response = self.kernel.run_function(test__return_type__table_response, {
            'arg': 'test'
        })

        self.assertTrue(
            '+------' in response.first()
        )

        response = self.kernel.run_function(test__return_type__table_response, {
            'arg': 'test'
        }, render_mode=KERNEL_RENDER_MODE_JSON)

        self.assertTrue(
            'body' in response.first()
        )
