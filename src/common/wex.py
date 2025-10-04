from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.decorator.base_class import base_class
from wexample_wex_core.common.kernel import Kernel

if TYPE_CHECKING:
    from src.workdir.wex_workdir import WexWorkdir


@base_class
class Wex(Kernel):
    def _get_workdir_state_manager_class(self) -> type[WexWorkdir]:
        from src.workdir.wex_workdir import WexWorkdir
        return WexWorkdir

    def exec(self):
        try:
            from wexample_wex_addon_dev_php.php_addon_manager import (
                PhpAddonManager,
            )
            from wexample_wex_addon_dev_javascript.javascript_addon_manager import (
                JavascriptAddonManager,
            )
            from wexample_wex_addon_dev_python.python_addon_manager import (
                PythonAddonManager,
            )
            from wexample_wex_core.addons.default.default_addon_manager import (
                DefaultAddonManager,
            )
            # from wexample_wex_core.addons.test.test_addon_manager import TestAddonManager
            from wexample_wex_core.common.kernel import Kernel
            from wexample_wex_addon_filestate.filestate_addon_manager import FilestateAddonManager
            from wexample_wex_addon_app.app_addon_manager import AppAddonManager

            self.setup(addons=[
                AppAddonManager,
                DefaultAddonManager,
                FilestateAddonManager,
                JavascriptAddonManager,
                PhpAddonManager,
                PythonAddonManager,
                # TODO Add it only when testing core.
                # TestAddonManager,
            ]).exec_argv()

        except Exception as e:
            from wexample_app.helpers.debug import debug_handle_app_error

            debug_handle_app_error(e)
