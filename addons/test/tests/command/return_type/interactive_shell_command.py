import json
from typing import Optional

from addons.test.command.return_type.interactive_shell_command import (
    test__return_type__interactive_shell_command,
)
from src.const.globals import (
    KERNEL_RENDER_MODE_JSON,
    KERNEL_RENDER_MODE_NONE,
    KERNEL_RENDER_MODE_TERMINAL,
)
from tests.AbstractTestCase import AbstractTestCase


class TestTestCommandReturnTypeInteractiveShellCommand(AbstractTestCase):
    def test_interactive_shell_command(self) -> None:
        self.for_each_render_mode(
            self._test_interactive_shell_command,
            {
                KERNEL_RENDER_MODE_NONE: None,
                KERNEL_RENDER_MODE_JSON: json.dumps(
                    {"value": ["INTERACTIVE_SHELL_COMMAND_RESPONSE"]}
                ),
                KERNEL_RENDER_MODE_TERMINAL: "INTERACTIVE_SHELL_COMMAND_RESPONSE",
            },
        )

    def _test_interactive_shell_command(self, render_mode: str) -> Optional[str]:
        return self.kernel.run_function(
            test__return_type__interactive_shell_command, render_mode=render_mode
        ).print_wrapped(render_mode)
