import re

from addons.app.command.script.exec import app__script__exec
from addons.app.decorator.option_webhook_url import option_webhook_url
from addons.app.AppAddonManager import AppAddonManager
from urllib.parse import urlparse, parse_qs
from addons.core.command.logs.rotate import core__logs__rotate
from src.const.globals import VERBOSITY_LEVEL_QUIET
from src.core.Kernel import Kernel
from src.decorator.command import command
from src.decorator.verbosity import verbosity
from src.decorator.option import option
from src.core.response.QueuedCollectionResponse import QueuedCollectionResponse
from src.core.response.queue_collection.QueuedCollectionStopResponse import QueuedCollectionStopResponse
from src.core.response.HiddenResponse import HiddenResponse


@command(help="Execute a webhook")
@verbosity(VERBOSITY_LEVEL_QUIET)
@option_webhook_url()
@option('--env', '-e', type=str, required=False, help="Env directory")
def app__webhook__exec(kernel: Kernel, url: str, env: None | str = None):
    from addons.app.command.webhook.listen import WEBHOOK_LISTENER_ROUTES_MAP

    source_data = {}
    parsed_url = urlparse(url)
    path = parsed_url.path
    match = re.match(
        WEBHOOK_LISTENER_ROUTES_MAP['exec']['pattern'],
        path
    )

    if not match:
        return

    app_name, webhook = match.groups()

    def _cleanup():
        kernel.run_function(core__logs__rotate)

    def _check(previous):
        query_string = parsed_url.query.replace('+', '%2B')
        query_string_data = parse_qs(query_string)
        has_error = False

        # Get all query parameters
        args = []

        for key, value in query_string_data.items():
            # Prevent risky data.
            if re.search(r'[^a-zA-Z0-9_\-]', key):
                has_error = True
                source_data['invalid_key'] = key

            if re.search(r'[^a-zA-Z0-9_\-\\.~\\+]', value[0]):
                has_error = True
                source_data['invalid_value'] = value[0]

            args.append(f'-{key}')
            # Use only the first value for each key
            args.append(value[0])

        if not has_error:
            manager = AppAddonManager(kernel)
            apps = manager.get_proxy_apps()

            # App exists somewhere.
            if app_name in apps:
                return HiddenResponse(kernel, apps[app_name])

        kernel.logger.append_event('EVENT_WEBHOOK_EXEC', {
            'url': url,
            'source_data': source_data,
            'success': False
        })

        return QueuedCollectionStopResponse(kernel)

    def _execute(previous: str):
        manager = AppAddonManager(kernel)
        manager.set_app_workdir(previous)
        source_data['app_dir'] = manager.app_dir

        response = kernel.run_function(
            app__script__exec,
            {
                'name': webhook,
                'app-dir': manager.app_dir,
            }
        )

        return response

    def _log(previous):
        kernel.logger.append_event('EVENT_WEBHOOK_EXEC', {
            'url': url,
            'source_data': source_data,
            'success': True
        })

    return QueuedCollectionResponse(kernel, [
        _cleanup,
        _check,
        _execute,
        _log,
    ])
