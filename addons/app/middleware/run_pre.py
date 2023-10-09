from src.const.globals import COMMAND_TYPE_ADDON
from addons.app.AppAddonManager import AppAddonManager


def app_middleware_run_pre(kernel, request) -> None:
    if request.type == COMMAND_TYPE_ADDON:
        addon, group, name = request.match.groups()
        if addon == 'app':
            manager: AppAddonManager = kernel.addons['app']

            manager.command_run_pre(
                request
            )
