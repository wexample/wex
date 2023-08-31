import os

from src.const.globals import COMMAND_TYPE_ADDON


def app_middleware_exec(
        kernel, *,
        match=None,
        command=None,
        command_type: str = None,
        args=None,
        args_list=[],
        function,
        **kwargs) -> None:
    if command_type == COMMAND_TYPE_ADDON:
        addon, group, name = match.groups()

        if addon == 'app':
            kernel.addons['app'].command_exec_pre(
                function,
                args,
                command,
                args_list)
