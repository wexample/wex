import json

from addons.test.command.return_type.table import test__return_type__table
from src.const.globals import (
    KERNEL_RENDER_MODE_JSON,
    KERNEL_RENDER_MODE_NONE,
    KERNEL_RENDER_MODE_TERMINAL,
)
from tests.AbstractTestCase import AbstractTestCase


class TestTestCommandReturnTypeTable(AbstractTestCase):
    def test_table(self) -> None:
        self.for_each_render_mode(
            self._test_table,
            {
                KERNEL_RENDER_MODE_NONE: None,
            },
        )

    def _test_table(self, render_mode) -> str | None:
        response = self.kernel.run_function(
            test__return_type__table, {"arg": "test"}, render_mode=render_mode
        )

        if render_mode == KERNEL_RENDER_MODE_TERMINAL:
            self.assertResponseFirstContains(response, "+------")
        elif render_mode == KERNEL_RENDER_MODE_JSON:
            self.assertResponseFirstContains(response, "body")

            data = json.loads(response.print_wrapped(render_mode))

            self.assertIsDict(data)
            self.assertIsList(data["body"])

        return response.print_wrapped(render_mode)
