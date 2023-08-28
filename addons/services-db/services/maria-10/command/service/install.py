import click

from addons.app.helpers.app import config_save
from addons.app.decorator.app_dir_option import app_dir_option
from src.const.globals import PASSWORD_INSECURE


@click.command()
@click.pass_obj
@app_dir_option()
def maria_10__service__install(kernel, app_dir:str):
    name = kernel.addons['app']['config']['global']['name']

    kernel.addons['app']['config']['maria-10'] = {
        'host': f'{name}_maria_10',
        'name': f'{name}',
        'password': PASSWORD_INSECURE,
        'port': 3306,
        'user': 'root',
    }

    config_save(kernel, app_dir)
