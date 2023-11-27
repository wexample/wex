import json

from addons.test.command.return_type.hidden import test__return_type__hidden
from src.const.globals import (
    KERNEL_RENDER_MODE_JSON,
    KERNEL_RENDER_MODE_NONE,
    KERNEL_RENDER_MODE_TERMINAL,
)
from tests.AbstractTestCase import AbstractTestCase


class TestTestCommandReturnTypeHidden(AbstractTestCase):
    def test_hidden(self):
        self.for_each_render_mode(
            self._test_hidden,
            {
                KERNEL_RENDER_MODE_NONE: None,
                KERNEL_RENDER_MODE_JSON: json.dumps({"value": None}),
                KERNEL_RENDER_MODE_TERMINAL: None,
            },
        )

    def _test_hidden(self, render_mode):
        response = self.kernel.run_function(
            test__return_type__hidden, render_mode=render_mode
        )

        self.assertIsNone(
            # Not displayed when interactive data
            response.print(interactive_data=True)
        )

        return response.print_wrapped(render_mode)
