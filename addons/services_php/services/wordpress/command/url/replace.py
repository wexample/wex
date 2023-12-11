import re
from typing import TYPE_CHECKING, Optional

import click

from addons.app.command.app.exec import app__app__exec
from addons.app.command.db.exec import app__db__exec
from addons.app.const.app import APP_NO_SSL_ENVS
from addons.app.decorator.app_command import app_command
from src.const.globals import COMMAND_TYPE_SERVICE
from src.core.response.AbstractResponse import ResponseCollection
from src.core.response.HiddenResponse import HiddenResponse
from src.core.response.queue_collection.AbstractQueuedCollectionResponseQueueManager import (
    AbstractQueuedCollectionResponseQueueManager,
)
from src.core.response.queue_collection.QueuedCollectionStopResponse import (
    QueuedCollectionStopResponse,
)
from src.core.response.QueuedCollectionResponse import QueuedCollectionResponse
from src.decorator.option import option

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(
    help="Change wordpress URL in database",
    command_type=COMMAND_TYPE_SERVICE,
    should_run=True,
)
@option(
    "--new-url",
    "-nu",
    type=str,
    required=False,
    help="New URL with trailing slash : (ex: http://wexample.com/)",
)
@option(
    "--old-url",
    "-ou",
    type=str,
    required=False,
    help="Old URL with trailing slash : (ex: http://wexample.com/)",
)
@option(
    "--site-id",
    "-si",
    type=int,
    required=False,
    default=1,
    help="WordPress Multisite ID. Default is 1.",
)
@option(
    "--yes",
    "-y",
    type=bool,
    is_flag=True,
    required=False,
    help="Do not ask for confirmation",
)
def wordpress__url__replace(
    manager: "AppAddonManager",
    app_dir: str,
    service: str,
    new_url: None | str = None,
    old_url: None | str = None,
    site_id: int = 1,
    yes: bool = False,
) -> HiddenResponse | QueuedCollectionResponse:
    kernel = manager.kernel

    def _build_urls(
        queue: AbstractQueuedCollectionResponseQueueManager,
    ) -> Optional[HiddenResponse | QueuedCollectionStopResponse]:
        nonlocal new_url
        nonlocal old_url

        # Determine table prefix based on site ID
        base_prefix = manager.get_config(f"service.{service}.db_prefix").get_str()
        prefix = f"{base_prefix}{site_id}_" if site_id > 1 else base_prefix

        if not new_url:
            env = manager.get_runtime_config("env").get_str()
            protocol = f'http{"" if env in APP_NO_SSL_ENVS else "s"}'
            new_url = (
                protocol + "://" + manager.get_runtime_config("domain_main").get_str()
            )

        assert isinstance(new_url, str)

        new_url = wordpress__url__replace__prepare_url(manager, new_url)
        if not new_url:
            return QueuedCollectionStopResponse(kernel, "WORDPRESS_MISSING_NEW_URL")

        if not old_url:
            sql = f"SELECT option_value FROM {prefix}options WHERE option_name = 'siteurl'"

            response = kernel.run_function(
                app__db__exec,
                {
                    "app-dir": app_dir,
                    # Ask to execute bash
                    "command": sql,
                    "sync": True,
                },
            )

            first = response.first()
            if not first:
                return None

            if len(first):
                old_url = first[0]

        assert isinstance(old_url, str)

        old_url = wordpress__url__replace__prepare_url(manager, old_url)
        if not old_url:
            return QueuedCollectionStopResponse(kernel, "WORDPRESS_MISSING_OLD_URL")

        app_name = manager.get_config("global.name").get_str()
        message_part = f'old url {old_url} (https, http, and domain only) by new url {new_url} in "{app_name}"'
        if not yes and not click.confirm(
            f"Are you ready to rewrite {message_part}", default=True
        ):
            return QueuedCollectionStopResponse(
                kernel, "WORDPRESS_REPLACEMENT_USER_ABORT"
            )

        kernel.io.log(f"Rewriting {message_part}...")

        # Create map
        url_map = {
            old_url: new_url,
            old_url.replace("https://", "http://"): new_url,
            old_url.replace("https://", "")
            .replace("http://", ""): new_url.replace("https://", "")
            .replace("http://", ""),
        }

        return HiddenResponse(kernel, url_map)

    def _replace(
        queue: AbstractQueuedCollectionResponseQueueManager,
    ) -> QueuedCollectionResponse:
        responses: ResponseCollection = []
        previous = queue.get_previous_value()
        assert isinstance(previous, dict)

        if previous:
            for old_url in previous:
                new_url = previous[old_url]

                responses.append(
                    kernel.run_function(
                        app__app__exec,
                        {
                            "app-dir": app_dir,
                            "container-name": "wordpress_cli",
                            "command": [
                                "wp",
                                "search-replace",
                                old_url,
                                new_url,
                                "--skip-columns=guid",
                            ],
                        },
                    )
                )

                kernel.io.message(f"Replaced {old_url} by {new_url}")

        return QueuedCollectionResponse(kernel, responses)

    return QueuedCollectionResponse(kernel, [_build_urls, _replace])


def wordpress__url__replace__prepare_url(
    manager: "AppAddonManager", url: str
) -> Optional[str]:
    url = url.rstrip("/")  # Remove trailing slash

    if not wordpress__url__replace__is_valid_url(url):
        manager.kernel.io.log(f"Invalid url {url}")
        return None

    return url


def wordpress__url__replace__is_valid_url(url: str) -> bool:
    pattern = re.compile(
        r"^https?://(?:[a-zA-Z0-9-]+\.)*[a-zA-Z0-9-]+\.[a-zA-Z]+(?::\d+)?/?$"
    )
    return bool(pattern.match(url))
