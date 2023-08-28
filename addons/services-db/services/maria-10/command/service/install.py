import click

from addons.app.helpers.app import config_save
from src.const.globals import PASSWORD_INSECURE


@click.command()
@click.pass_obj
def maria_10__service__install(kernel):
    name = kernel.addons['app']['config']['global']['name']

    kernel.addons['app']['config']['maria-10'] = {
        'host': f'{name}_maria_10',
        'name': f'{name}',
        'password': PASSWORD_INSECURE,
        'port': 3306,
        'user': 'root',
    }

    config_save(kernel, kernel.addons['app']['config']['context']['dir'])
