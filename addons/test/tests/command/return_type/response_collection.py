import json
from typing import Optional

from addons.test.command.return_type.response_collection import (
    test__return_type__response_collection,
)
from src.const.globals import (
    KERNEL_RENDER_MODE_JSON,
    KERNEL_RENDER_MODE_NONE,
    KERNEL_RENDER_MODE_TERMINAL,
)
from tests.AbstractTestCase import AbstractTestCase


class TestTestCommandReturnTypeResponseCollection(AbstractTestCase):
    def test_response_collection(self) -> None:
        self.for_each_render_mode(
            self._test_response_collection,
            {
                KERNEL_RENDER_MODE_NONE: None,
                KERNEL_RENDER_MODE_JSON: json.dumps(
                    [
                        "DEFAULT",
                        {"lorem": "ipsum"},
                        "FUNCTION_OK",
                        None,
                        "INTERACTIVE_SHELL_COMMAND_RESPONSE",
                        {"key": "value"},
                        "NON_INTERACTIVE_SHELL_COMMAND_RESPONSE",
                        None,
                        {
                            "body": [["lorem", "ipsum"], ["dolor", "sit"]],
                            "header": [],
                            "title": "Test Table",
                        },
                    ]
                ),
                KERNEL_RENDER_MODE_TERMINAL: """DEFAULT
lorem: ipsum
FUNCTION_OK
INTERACTIVE_SHELL_COMMAND_RESPONSE
key : value

NON_INTERACTIVE_SHELL_COMMAND_RESPONSE
== Test Table ===
+---------------+
| lorem | ipsum |
| dolor | sit   |
+---------------+
""",
            },
        )

    def _test_response_collection(self, render_mode: str) -> Optional[str]:
        return self.kernel.run_function(
            function=test__return_type__response_collection, render_mode=render_mode
        ).print_wrapped(render_mode)
