from src.core.response.AbstractResponse import AbstractResponse
from src.const.globals import COMMAND_TYPE_ADDON
from addons.app.AppAddonManager import AppAddonManager


def app_middleware_run_post(kernel, request, response: AbstractResponse) -> None:
    if request.type == COMMAND_TYPE_ADDON:
        addon, group, name = request.match.groups()

        # This is an app::xxx/yyy command.
        if addon == 'app':
            manager: AppAddonManager = kernel.addons['app']

            manager.command_run_post(
                request
            )
