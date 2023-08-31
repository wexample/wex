from src.const.globals import COMMAND_TYPE_ADDON


def app_middleware_exec_post(kernel, *,
                             match=None,
                             command_type: str,
                             function,
                             **kwargs) -> None:
    if command_type == COMMAND_TYPE_ADDON:
        addon, group, name = match.groups()

        if addon == 'app':
            kernel.addons['app'].command_exec_post(function)
