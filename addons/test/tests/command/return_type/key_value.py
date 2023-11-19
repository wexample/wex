import json
import os

from addons.test.command.return_type.key_value import test__return_type__key_value
from src.const.globals import KERNEL_RENDER_MODE_NONE, KERNEL_RENDER_MODE_JSON, KERNEL_RENDER_MODE_TERMINAL
from tests.AbstractTestCase import AbstractTestCase


class TestTestCommandReturnTypeKeyValue(AbstractTestCase):
    def test_key_value(self):
        self.for_each_render_mode(self._test_key_value, {
            KERNEL_RENDER_MODE_NONE: None,
            KERNEL_RENDER_MODE_JSON: json.dumps({'str': 'lorem', 'int': 123, 'bool': True}),
            KERNEL_RENDER_MODE_TERMINAL: f'str  : lorem{os.linesep}int  : 123{os.linesep}bool : True{os.linesep}',
        })

    def _test_key_value(self, render_mode):
        response = self.kernel.run_function(
            test__return_type__key_value,
            render_mode=render_mode)

        return response.print_wrapped(render_mode)
