import os

from src.const.globals import COMMAND_TYPE_ADDON


def app_middleware_run_pre(kernel, processor) -> None:
    if processor.command_type == COMMAND_TYPE_ADDON:
        addon, group, name = processor.match.groups()
        if addon == 'app':
            kernel.addons['app'].command_run_pre(
                processor
            )
