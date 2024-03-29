import re
from typing import TYPE_CHECKING, Optional
from urllib.parse import parse_qsl, urlparse

from addons.app.decorator.option_webhook_listener import option_webhook_listener
from src.core.response.AbstractResponse import AbstractResponse
from src.core.response.queue_collection.AbstractQueuedCollectionResponseQueueManager import (
    AbstractQueuedCollectionResponseQueueManager,
)
from src.core.response.queue_collection.QueuedCollectionStopResponse import (
    QueuedCollectionStopResponse,
)
from src.core.response.QueuedCollectionResponse import QueuedCollectionResponse
from src.decorator.command import command
from src.decorator.option import option

if TYPE_CHECKING:
    from src.core.Kernel import Kernel

from typing import TypedDict


class SourceData(TypedDict, total=False):
    invalid_key: str
    invalid_value: str


@command(help="Execute a webhook")
@option_webhook_listener(path=True)
@option("--env", "-e", type=str, required=False, help="Env directory")
def app__webhook__exec(
    kernel: "Kernel", webhook_path: str, env: None | str = None
) -> Optional[QueuedCollectionResponse]:
    from addons.app.const.webhook import WEBHOOK_LISTENER_ROUTES_MAP

    source_data: SourceData = {}
    parsed_url = urlparse(webhook_path)
    path = parsed_url.path
    match = re.match(WEBHOOK_LISTENER_ROUTES_MAP["exec"]["pattern"], path)
    query_string = parsed_url.query.replace("+", "%2B")
    query_string_data = dict(parse_qsl(query_string))

    if not match or len(match.groups()) < 2:
        kernel.logger.append_event(
            "WEBHOOK_PATH_DOES_NOT_MATCH",
            {
                "path": path,
            },
        )

        return None

    command_type = str(match.group(1))

    if not command_type in kernel.resolvers:
        kernel.logger.append_event(
            "WEBHOOK_RESOLVER_NOT_FOUND",
            {
                "command_type": command_type,
            },
        )

        return None

    command_path = str(match.group(2))

    def _check(
        queue: AbstractQueuedCollectionResponseQueueManager,
    ) -> Optional[AbstractResponse]:
        has_error = False
        # Get all query parameters
        args = []

        for key, value in query_string_data.items():
            # Prevent risky data.
            if re.search(r"[^a-zA-Z0-9_\-]", key):
                has_error = True
                source_data["invalid_key"] = key

            if re.search(r"[^a-zA-Z0-9_\-\\.~\\+]", value[0]):
                has_error = True
                source_data["invalid_value"] = value[0]

            args.append(f"-{key}")
            # Use only the first value for each key
            args.append(value[0])

        if has_error:
            kernel.logger.append_event(
                "WEBHOOK_ERROR",
                {"path": path, "source_data": source_data, "success": False},
            )

            return QueuedCollectionStopResponse(kernel, "WEBHOOK_ERROR")

        return None

    def _execute(
        queue: AbstractQueuedCollectionResponseQueueManager,
    ) -> AbstractResponse:
        return kernel.get_command_resolver(
            command_type
        ).run_command_request_from_url_path(command_path, query_string_data)

    def _log(queue: AbstractQueuedCollectionResponseQueueManager) -> None:
        kernel.logger.append_event(
            "WEBHOOK_COMPLETE",
            {"path": path, "source_data": source_data, "success": True},
        )

    return QueuedCollectionResponse(
        kernel,
        [
            _check,
            _execute,
            _log,
        ],
    )
