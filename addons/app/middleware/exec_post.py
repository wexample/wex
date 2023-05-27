from addons.app.helpers.app import unset_app_workdir


def app_middleware_exec_post(kernel, *, addon=None, **kwargs) -> None:
    if addon == 'app':
        if hasattr(kernel.addons[addon]['config'], 'context') \
                and hasattr(kernel.addons[addon]['config']['context'],
                            'call_command_level'):
            kernel.addons[addon]['config']['context']['call_command_level'] -= 0

            if kernel.addons[addon]['config']['context']['call_command_level'] <= 0:
                unset_app_workdir(kernel)
