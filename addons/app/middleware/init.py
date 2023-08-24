import os
import platform

from addons.app.const.app import PROXY_APP_NAME, PROXY_FILE_APPS_REGISTRY
from src.helper.file import yaml_load_or_default
from addons.app.command.location.find import app__location__find


def app_middleware_init(kernel, **kwargs) -> None:
    port = 80
    port_secure = 443

    if platform.system() == 'Darwin':
        proxy_dir = '/Users/.wex/server/'
        port = 4242
        port_secure = 4243
    else:
        proxy_dir = '/opt/{}/'.format(PROXY_APP_NAME)

    kernel.addons['app'] = {**kernel.addons['app'], **{
        'path': {
            'proxy': proxy_dir,
            'call_app_dir': app__location__find.callback(
                os.getcwd()
            )
        },
        'proxy': {
            'apps': yaml_load_or_default(proxy_dir + PROXY_FILE_APPS_REGISTRY, [])
        }
    }}
