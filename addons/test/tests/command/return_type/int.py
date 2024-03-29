from typing import Optional

from addons.test.command.return_type.int import test__return_type__int
from src.const.globals import (
    KERNEL_RENDER_MODE_JSON,
    KERNEL_RENDER_MODE_NONE,
    KERNEL_RENDER_MODE_TERMINAL,
)
from tests.AbstractTestCase import AbstractTestCase


class TestTestCommandReturnTypeInt(AbstractTestCase):
    def test_int(self) -> None:
        self.for_each_render_mode(
            self._test_int,
            {
                KERNEL_RENDER_MODE_NONE: None,
                KERNEL_RENDER_MODE_JSON: 11,
                KERNEL_RENDER_MODE_TERMINAL: 11,
            },
        )

    def _test_int(self, render_mode: str) -> Optional[int]:
        response = self.kernel.run_function(
            test__return_type__int,
            {
                "arg": 10,
            },
            render_mode=render_mode,
        )

        output = response.print()

        try:
            return output if isinstance(output, int) else None
        except ValueError:
            return None
