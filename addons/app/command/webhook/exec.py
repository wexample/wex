import re

from addons.app.command.script.exec import app__script__exec
from urllib.parse import urlparse, parse_qs
from addons.core.command.logs.rotate import core__logs__rotate
from src.core.response.DictResponse import DictResponse
from src.core.Kernel import Kernel
from src.decorator.command import command
from src.decorator.option import option
from addons.app.AppAddonManager import AppAddonManager
from src.core.response.QueuedCollectionResponse import QueuedCollectionResponse
from src.core.response.ResponseCollectionStopResponse import ResponseCollectionStopResponse
from src.core.response.HiddenResponse import HiddenResponse


@command(help="Execute a webhook")
@option('--url', '-u', type=str, required=True, help="Argument")
@option('--env', '-e', type=str, required=False, help="Env directory")
def app__webhook__exec(kernel: Kernel, url: str, env: None | str = None):
    source_data = {}
    parsed_url = urlparse(url)
    path = parsed_url.path

    if path == '/status':
        response = DictResponse(kernel)
        response.set_dictionary({
            'running': True
        })
        return response

    pattern = r'^\/webhook/([a-zA-Z_\-]+)/([a-zA-Z_\-]+)$'
    match = re.match(pattern, path)

    kernel.run_function(core__logs__rotate)

    if not match:
        return

    app_name, webhook = match.groups()

    def _check():
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

        return ResponseCollectionStopResponse(kernel)

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
        ).first()

        kernel.logger.append_event('EVENT_WEBHOOK_EXEC', {
            'url': url,
            'source_data': source_data,
            'success': True
        })

        return response

    return QueuedCollectionResponse(kernel, [
        _check,
        _execute
    ])
