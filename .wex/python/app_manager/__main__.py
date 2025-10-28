#!/usr/bin/env python3
"""Main entry point for the application."""
from wexample_wex_core.common.app_manager_kernel import AppManagerKernel

if __name__ == "__main__":
    try:
        from wexample_wex_addon_dev_python.python_addon_manager import (
            PythonAddonManager,
        )
        from wexample_wex_core.addons.default.default_addon_manager import (
            DefaultAddonManager,
        )
        from wexample_wex_core.addons.git.git_addon_manager import (
            GitAddonManager,
        )
        from wexample_wex_core.common.kernel import Kernel
        from wexample_wex_addon_filestate.filestate_addon_manager import FilestateAddonManager
        from wexample_wex_addon_app.app_addon_manager import AppAddonManager

        (
            AppManagerKernel(
                entrypoint_path=__file__,
            )
            .setup(addons=[
                AppAddonManager,
                DefaultAddonManager,
                GitAddonManager,
            ])
            .exec_argv()
        )
    except Exception as e:
        from wexample_app.helpers.debug import debug_handle_app_error

        debug_handle_app_error(e)
