from src.const.globals import COMMAND_TYPE_ADDON


def app_middleware_run_post(kernel, request) -> None:
    if request.type == COMMAND_TYPE_ADDON:
        addon, group, name = request.match.groups()

        # This is an app::xxx/yyy command.
        if addon == 'app':
            kernel.addons['app'].command_run_post(
                request
            )
