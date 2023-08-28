import click
import platform

from addons.app.const.app import PROXY_APP_NAME
from addons.app.helpers.app import config_save


@click.command()
@click.pass_obj
def proxy__service__install(kernel):
    port = 80
    port_secure = 443

    # MacOS changes (not tested inherited code)
    if platform.system() == 'Darwin':
        proxy_dir = '/Users/.wex/server/'
        port = 7780
        port_secure = 7743
    else:
        proxy_dir = '/opt/{}/'.format(PROXY_APP_NAME)

    kernel.addons['app']['config']['global'].update({
        'port_public': port,
        'port_public_secure': port_secure,
    })

    kernel.addons['app']['config']['path'].update({
        'proxy': proxy_dir
    })

    config_save(kernel, kernel.addons['app']['config']['context']['dir'])
