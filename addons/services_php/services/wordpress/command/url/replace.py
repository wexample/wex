import re
import click

from addons.app.const.app import APP_NO_SSL_ENVS
from src.decorator.option import option
from src.core import Kernel
from addons.app.AppAddonManager import AppAddonManager
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE
from addons.app.command.db.exec import app__db__exec


@app_command(help="Change wordpress URL in database", command_type=COMMAND_TYPE_SERVICE, should_run=True)
@option('--new-url', '-nu', type=str, required=False, help="New URL with trailing slash : (ex: http://wexample.com/)")
@option('--old-url', '-ou', type=str, required=False, help="Old URL with trailing slash : (ex: http://wexample.com/)")
def wordpress__url__replace(kernel: Kernel,
                            app_dir: str,
                            service: str,
                            new_url: None | str = None,
                            old_url: None | str = None):
    manager: AppAddonManager = kernel.addons['app']

    if not new_url:
        env = manager.get_runtime_config('env')
        protocol = f'http{"s" if env in APP_NO_SSL_ENVS else ""}'
        new_url = protocol + '://' + manager.get_runtime_config('domain_main')

    new_url = wordpress__url__replace__prepare_url(new_url)
    if not new_url:
        return

    if not old_url:
        prefix = manager.get_config(f'service.{service}.db_prefix')
        sql = f"SELECT option_value FROM {prefix}options WHERE option_name = 'siteurl'"

        response = kernel.run_function(
            app__db__exec,
            {
                'app-dir': app_dir,
                # Ask to execute bash
                'command': sql,
                'sync': True
            }
        )

        first = response.first()
        if len(first):
            old_url = first[0]

    old_url = wordpress__url__replace__prepare_url(old_url)
    if not old_url:
        return

    app_name = manager.get_config('global.name')
    if click.confirm(
            f'Are you ready to rewrite old url {old_url} by new url {new_url} in "{app_name}"',
            default=True):
        return False


def wordpress__url__replace__prepare_url(url) -> bool | str:
    url = url if url.endswith('/') else url + '/'

    if not wordpress__url__replace__is_valid_url(url):
        url.io.log(f'Invalid url {url}')
        return False

    return url


def wordpress__url__replace__is_valid_url(url) -> bool:
    pattern = re.compile(r'^https?://(?:[a-zA-Z0-9-]+\.)*[a-zA-Z0-9-]+\.[a-zA-Z]+(?::\d+)?/$')
    return bool(pattern.match(url))
