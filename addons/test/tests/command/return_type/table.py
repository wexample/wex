from addons.test.command.return_type.table import test__return_type__table
from src.const.globals import KERNEL_RENDER_MODE_HTTP
from tests.AbstractTestCase import AbstractTestCase


class TestTestCommandReturnTypeTable(AbstractTestCase):
    def test_table(self):
        response = self.kernel.run_function(test__return_type__table, {
            'arg': 'test'
        })

        self.assertTrue(
            '+------' in response.first()
        )

        response = self.kernel.run_function(test__return_type__table, {
            'arg': 'test'
        }, render_mode=KERNEL_RENDER_MODE_HTTP)

        self.assertTrue(
            'body' in response.first()
        )
