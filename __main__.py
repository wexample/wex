#!/usr/bin/env python3
"""Main entry point for the application."""

if __name__ == '__main__':
    try:
        from wexample_wex_core.common.kernel import Kernel
        from wexample_wex_core.addons.default.default_addon_manager import DefaultAddonManager

        (Kernel(
            entrypoint_path=__file__,
            addons=[
                DefaultAddonManager
            ])
         .exec_argv())
    except Exception as e:
        from wexample_app.helpers.debug import debug_handle_app_error

        debug_handle_app_error(e)
