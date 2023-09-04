import os

from src.const.globals import COMMAND_TYPE_ADDON


def app_middleware_run_pre(kernel, request) -> None:
    if request.type == COMMAND_TYPE_ADDON:
        addon, group, name = request.match.groups()
        if addon == 'app':
            kernel.addons['app'].command_run_pre(
                request
            )
