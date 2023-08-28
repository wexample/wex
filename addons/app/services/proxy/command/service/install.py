import click
import platform

from addons.app.const.app import PROXY_APP_NAME
from addons.app.helpers.app import config_save
from addons.app.decorator.app_dir_option import app_dir_option


@click.command()
@click.pass_obj
@app_dir_option()
def proxy__service__install(kernel, app_dir:str):
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

    config_save(kernel, app_dir)
