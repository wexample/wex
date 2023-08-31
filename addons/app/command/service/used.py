from __future__ import annotations

import click

from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.AppAddonManager import AppAddonManager


@click.command()
@click.pass_obj
@app_dir_option()
@click.option('--service', '-s', type=str, required=True,
              help="Service name to check in app configuration")
def app__service__used(kernel, service, app_dir):
    manager: 'AppAddonManager' = kernel.addons['app']

    return manager.get_config('global.services')
