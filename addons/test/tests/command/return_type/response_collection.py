from addons.test.command.return_type.response_collection import test__return_type__response_collection
from src.const.globals import KERNEL_RENDER_MODE_NONE, KERNEL_RENDER_MODE_JSON, KERNEL_RENDER_MODE_TERMINAL
from tests.AbstractTestCase import AbstractTestCase
import json


class TestTestCommandReturnTypeResponseCollection(AbstractTestCase):
    def test_response_collection(self):
        self.for_each_render_mode(self._test_response_collection, {
            KERNEL_RENDER_MODE_NONE: None,
            KERNEL_RENDER_MODE_JSON: json.dumps({'value': None}),
            KERNEL_RENDER_MODE_TERMINAL: None,
        })

    def _test_response_collection(self, render_mode):
        return self.kernel.run_function(
            function=test__return_type__response_collection,
            render_mode=render_mode).print_wrapped(render_mode)
