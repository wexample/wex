import re
import click

from addons.app.const.app import APP_NO_SSL_ENVS
from src.core.response.queue_collection.QueuedCollectionStopResponse import QueuedCollectionStopResponse
from src.core.response.HiddenResponse import HiddenResponse
from src.decorator.option import option
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE
from addons.app.command.db.exec import app__db__exec
from addons.app.command.app.exec import app__app__exec
from src.core.response.QueuedCollectionResponse import QueuedCollectionResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(help="Change wordpress URL in database", command_type=COMMAND_TYPE_SERVICE, should_run=True)
@option('--new-url', '-nu', type=str, required=False, help="New URL with trailing slash : (ex: http://wexample.com/)")
@option('--old-url', '-ou', type=str, required=False, help="Old URL with trailing slash : (ex: http://wexample.com/)")
@option('--site-id', '-si', type=int, required=False, default=1, help="WordPress Multisite ID. Default is 1.")
@option('--yes', '-y', type=bool, is_flag=True, required=False, help="Do not ask for confirmation")
def wordpress__url__replace(manager: 'AppAddonManager',
                            app_dir: str,
                            service: str,
                            new_url: None | str = None,
                            old_url: None | str = None,
                            site_id: int = 1,
                            yes: bool = False):
    kernel = manager.kernel

    def _build_urls():
        nonlocal new_url
        nonlocal old_url

        # Determine table prefix based on site ID
        base_prefix = manager.get_config(f'service.{service}.db_prefix')
        prefix = f"{base_prefix}{site_id}_" if site_id > 1 else base_prefix

        if not new_url:
            env = manager.get_runtime_config('env')
            protocol = f'http{"" if env in APP_NO_SSL_ENVS else "s"}'
            new_url = protocol + '://' + manager.get_runtime_config('domain_main')

        new_url = wordpress__url__replace__prepare_url(kernel, new_url)
        if not new_url:
            return QueuedCollectionStopResponse(kernel)

        if not old_url:
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
            if not first:
                return
            
            if len(first):
                old_url = first[0]

        old_url = wordpress__url__replace__prepare_url(kernel, old_url)
        if not old_url:
            return QueuedCollectionStopResponse(kernel)

        app_name = manager.get_config('global.name')
        message_part = f'old url {old_url} (https, http, and domain only) by new url {new_url} in "{app_name}"'
        if not yes and not click.confirm(
                f'Are you ready to rewrite {message_part}',
                default=True):
            return QueuedCollectionStopResponse(kernel)

        kernel.io.log(f'Rewriting {message_part}...')

        # Create map
        url_map = {
            old_url: new_url,
            old_url.replace("https://", "http://"): new_url,
            old_url.replace("https://", "").replace("http://", ""): new_url.replace("https://", "").replace("http://",
                                                                                                            "")
        }

        return HiddenResponse(kernel, url_map)

    def _replace(previous):
        responses = []

        if previous:
            for old_url in previous:
                new_url = previous[old_url]

                responses.append(kernel.run_function(
                    app__app__exec,
                    {
                        'app-dir': app_dir,
                        'container-name': 'wordpress_cli',
                        'command': [
                            'wp', 'search-replace',
                            old_url, new_url,
                            '--skip-columns=guid',
                        ]
                    }
                ))

                kernel.io.message(f'Replaced {old_url} by {new_url}')

        return QueuedCollectionResponse(kernel, responses)

    return QueuedCollectionResponse(kernel, [
        _build_urls,
        _replace
    ])


def wordpress__url__replace__prepare_url(manager: 'AppAddonManager', url) -> bool | str:
    url = url.rstrip('/')  # Remove trailing slash

    if not wordpress__url__replace__is_valid_url(url):
        manager.kernel.io.log(f'Invalid url {url}')
        return None

    return url


def wordpress__url__replace__is_valid_url(url) -> bool:
    pattern = re.compile(r'^https?://(?:[a-zA-Z0-9-]+\.)*[a-zA-Z0-9-]+\.[a-zA-Z]+(?::\d+)?/?$')
    return bool(pattern.match(url))
