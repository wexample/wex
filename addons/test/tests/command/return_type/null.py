import json

from addons.test.command.return_type.null import test__return_type__null
from src.const.globals import (
    KERNEL_RENDER_MODE_JSON,
    KERNEL_RENDER_MODE_NONE,
    KERNEL_RENDER_MODE_TERMINAL,
)
from tests.AbstractTestCase import AbstractTestCase


class TestTestCommandReturnTypeNull(AbstractTestCase):
    def test_null(self):
        self.for_each_render_mode(
            self._test_null,
            {
                KERNEL_RENDER_MODE_NONE: None,
                KERNEL_RENDER_MODE_JSON: json.dumps({"value": None}),
                KERNEL_RENDER_MODE_TERMINAL: None,
            },
        )

    def _test_null(self, render_mode):
        return self.kernel.run_function(
            function=test__return_type__null, render_mode=render_mode
        ).print_wrapped(render_mode)
