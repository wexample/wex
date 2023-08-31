from __future__ import annotations

import click

from addons.app.decorator.app_dir_option import app_dir_option
from addons.app.AppAddonManager import AppAddonManager
from src.decorator.command import command


@command()
@app_dir_option()
@click.option('--service', '-s', type=str, required=True,
              help="Service name to check in app configuration")
def app__service__used(kernel, service: str, app_dir: str) -> bool:
    manager: 'AppAddonManager' = kernel.addons['app']

    return service in manager.get_config('global.services')
