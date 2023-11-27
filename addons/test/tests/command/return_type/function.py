import json

from addons.test.command.return_type.function import test__return_type__function
from src.const.globals import (
    KERNEL_RENDER_MODE_JSON,
    KERNEL_RENDER_MODE_NONE,
    KERNEL_RENDER_MODE_TERMINAL,
)
from tests.AbstractTestCase import AbstractTestCase


class TestTestCommandReturnTypeFunction(AbstractTestCase):
    def test_function(self):
        self.for_each_render_mode(
            self._test_function,
            {
                KERNEL_RENDER_MODE_NONE: None,
                KERNEL_RENDER_MODE_TERMINAL: "FUNCTION_OK",
                KERNEL_RENDER_MODE_JSON: json.dumps({"value": "FUNCTION_OK"}),
            },
        )

    def _test_function(self, render_mode):
        response = self.kernel.run_function(
            test__return_type__function, {"arg": "test"}, render_mode=render_mode
        )

        return response.print_wrapped(render_mode)
