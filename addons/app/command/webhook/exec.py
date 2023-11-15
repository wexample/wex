import re

from addons.app.decorator.option_webhook_listener import option_webhook_listener
from urllib.parse import urlparse, parse_qs
from src.core.FunctionProperty import FunctionProperty
from src.core.Kernel import Kernel
from src.decorator.command import command
from src.decorator.option import option
from src.core.response.QueuedCollectionResponse import QueuedCollectionResponse
from src.core.response.queue_collection.QueuedCollectionStopResponse import QueuedCollectionStopResponse


@command(help="Execute a webhook")
@option_webhook_listener(path=True)
@option('--env', '-e', type=str, required=False, help="Env directory")
def app__webhook__exec(kernel: Kernel, path: str, env: None | str = None):
    from addons.app.command.webhook.listen import WEBHOOK_LISTENER_ROUTES_MAP

    source_data = {}
    parsed_url = urlparse(path)
    path = parsed_url.path
    match = re.match(
        WEBHOOK_LISTENER_ROUTES_MAP['exec']['pattern'],
        path
    )

    if not match:
        return

    command_type = match[1]
    resolver = kernel.get_command_resolver(command_type)

    if not resolver:
        return

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

        if has_error:
            kernel.logger.append_event('EVENT_WEBHOOK_EXEC', {
                'path': path,
                'source_data': source_data,
                'success': False
            })

            return QueuedCollectionStopResponse(kernel)

    def _execute(previous: str):
        path = match[2]

        request = kernel.create_command_request(
            resolver.create_command_from_path(
                path
            )
        )

        # Hooking this command is not allowed
        if not FunctionProperty.has_property(request.function, 'app_webhook'):
            return QueuedCollectionStopResponse(kernel)

        return resolver.run_command_request_from_url_path(path)

    def _log(previous):
        kernel.logger.append_event('EVENT_WEBHOOK_EXEC', {
            'path': path,
            'source_data': source_data,
            'success': True
        })

    return QueuedCollectionResponse(kernel, [
        _check,
        _execute,
        _log,
    ])
