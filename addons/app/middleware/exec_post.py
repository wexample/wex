from addons.app.helpers.app import unset_app_workdir


def app_middleware_exec_post(kernel, *, addon=None, **kwargs) -> None:
    if addon == 'app':
        if 'context' in kernel.addons[addon]['config'] \
                and 'call_command_level' in kernel.addons[addon]['config']['context']:
            kernel.addons[addon]['config']['context']['call_command_level'] -= 1

            if kernel.addons[addon]['config']['context']['call_command_level'] <= 0:
                unset_app_workdir(kernel)
