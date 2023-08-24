from addons.app.helpers.app import unset_app_workdir
from src.const.globals import COMMAND_TYPE_ADDON


def app_middleware_exec_post(kernel, *, match=None, command_type: str, **kwargs) -> None:
    if command_type == COMMAND_TYPE_ADDON:
        addon, group, name = match.groups()

        if addon == 'app':
            if 'context' in kernel.addons[addon]['config'] \
                    and 'call_command_level' in kernel.addons[addon]:
                kernel.addons[addon]['call_command_level'] -= 1

                if kernel.addons[addon]['call_command_level'] <= 0:
                    unset_app_workdir(kernel)
