import json

from addons.test.command.return_type.dict import test__return_type__dict
from src.const.globals import (
    KERNEL_RENDER_MODE_JSON,
    KERNEL_RENDER_MODE_NONE,
    KERNEL_RENDER_MODE_TERMINAL,
)
from tests.AbstractTestCase import AbstractTestCase


class TestTestCommandReturnTypeDict(AbstractTestCase):
    def test_dict(self) -> None:
        self.for_each_render_mode(
            self._test_dict,
            {
                KERNEL_RENDER_MODE_NONE: None,
                KERNEL_RENDER_MODE_JSON: json.dumps({"arg": "yes"}),
                KERNEL_RENDER_MODE_TERMINAL: "arg: yes",
            },
        )

    def _test_dict(self, render_mode):
        response = self.kernel.run_function(
            test__return_type__dict,
            {
                "arg": "yes",
            },
            render_mode=render_mode,
        )

        return response.print_wrapped(render_mode)
