import json
import os

from addons.test.command.return_type.queued_collection import (
    test__return_type__queued_collection,
)
from src.const.globals import (
    KERNEL_RENDER_MODE_JSON,
    KERNEL_RENDER_MODE_NONE,
    KERNEL_RENDER_MODE_TERMINAL,
)
from tests.AbstractTestCase import AbstractTestCase


class TestTestCommandReturnTypeQueuedCollection(AbstractTestCase):
    def test_queued_collection(self) -> None:
        self.for_each_render_mode(
            self._test_queued_collection,
            {
                KERNEL_RENDER_MODE_NONE: None,
                KERNEL_RENDER_MODE_JSON: json.dumps(
                    {"value": f"lorem{os.linesep}ipsum{os.linesep}123"}
                ),
                KERNEL_RENDER_MODE_TERMINAL: f"lorem{os.linesep}ipsum{os.linesep}123",
            },
        )

    def _test_queued_collection(self, render_mode) -> str | None:
        return self.kernel.run_function(
            function=test__return_type__queued_collection, render_mode=render_mode
        ).print_wrapped(render_mode)
