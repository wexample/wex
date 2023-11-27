import json

from addons.test.command.return_type.str import test__return_type__str
from src.const.globals import (
    KERNEL_RENDER_MODE_JSON,
    KERNEL_RENDER_MODE_NONE,
    KERNEL_RENDER_MODE_TERMINAL,
)
from tests.AbstractTestCase import AbstractTestCase


class TestTestCommandReturnTypeStr(AbstractTestCase):
    def test_str(self):
        self.for_each_render_mode(
            self._test_str,
            {
                KERNEL_RENDER_MODE_NONE: None,
                KERNEL_RENDER_MODE_JSON: json.dumps({"value": "yes"}),
                KERNEL_RENDER_MODE_TERMINAL: "yes",
            },
        )

    def _test_str(self, render_mode):
        response = self.kernel.run_function(
            test__return_type__str, {"arg": "yes"}, render_mode=render_mode
        )

        return response.print_wrapped(render_mode)
