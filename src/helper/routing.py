import re
from typing import Any, Dict, Optional, TypedDict, cast, TYPE_CHECKING
from urllib.parse import parse_qs, urlparse

from addons.app.typing.webhook import WebhookListenerRoutesMap
from src.const.types import StringKeysDict, StringsList
from addons.app.const.webhook import WEBHOOK_LISTENER_ROUTES_MAP
from src.const.globals import (
    COMMAND_TYPE_ADDON,
    KERNEL_RENDER_MODE_JSON,
)
from src.helper.command import command_get_option

if TYPE_CHECKING:
    from src.core.command.ScriptCommand import ScriptCommand

# Added an explicit whitelist for query parameters
ALLOWED_QUERY_NAME_CHARS = re.compile(r"^[a-zA-Z0-9_&]+$")
ALLOWED_QUERY_VALUE_CHARS = re.compile(r"^[a-zA-Z0-9_.+ \-]+$")


def routing_get_route_name(url: str, routes: Dict[str, Any]) -> Optional[str]:
    parsed_url = urlparse(url)
    path = parsed_url.path

    for route_name, config in routes.items():
        if re.match(config["pattern"], path):
            return route_name
    return None


class RouteInfo(TypedDict):
    is_async: bool
    name: str
    match: Optional[StringsList]
    query: StringKeysDict


def routing_get_route_info(
    url: str, routes: WebhookListenerRoutesMap
) -> Optional[RouteInfo]:
    route_name = routing_get_route_name(url, routes)
    if route_name:
        parsed_url = urlparse(url)
        path = parsed_url.path
        query = parse_qs(parsed_url.query)
        route = routes[route_name]
        pattern = route["pattern"]
        match = re.match(pattern, path)

        return RouteInfo(
            is_async=route["is_async"],
            name=route_name,
            match=cast(StringsList, match.groups()) if match else None,
            query=cast(StringKeysDict, query),
        )
    return None


def routing_is_allowed_route(url: str, routes: WebhookListenerRoutesMap) -> bool:
    route_info = routing_get_route_info(url, routes)

    if route_info:
        # Validate the query string to contain only allowed characters
        for key, values in route_info["query"].items():
            for value in values:
                if not ALLOWED_QUERY_NAME_CHARS.fullmatch(key) or not ALLOWED_QUERY_VALUE_CHARS.fullmatch(value):
                    return False
        return True
    return False


def routing_build_webhook_route_map(kernel):
    from addons.app.WebhookHttpRequestHandler import (
        WEBHOOK_COMMAND_PATH_PLACEHOLDER,
        WEBHOOK_COMMAND_PORT_PLACEHOLDER,
    )

    routes_map = WEBHOOK_LISTENER_ROUTES_MAP.copy()
    for route_name in routes_map:
        script_command: ScriptCommand = routes_map[route_name]["script_command"]
        options = {}
        needs_path = command_get_option(script_command, "webhook_path")
        needs_port_number = command_get_option(
            script_command, "webhook_port_number"
        )

        if needs_path:
            options["webhook_path"] = WEBHOOK_COMMAND_PATH_PLACEHOLDER

        if needs_port_number:
            options["webhook_port_number"] = WEBHOOK_COMMAND_PORT_PLACEHOLDER

        command_list = kernel.get_command_resolver(
            COMMAND_TYPE_ADDON
        ).build_full_command_parts_from_script_command(
            routes_map[route_name]["script_command"],
            options,
        )

        command_list += [
            "--parent-task-id",
            kernel.get_task_id(),
            # Allow parsing
            "--render-mode",
            KERNEL_RENDER_MODE_JSON,
            # No need to interact or create sub process
            "--fast-mode",
            # Avoid logging to be able to parse output
            "--quiet",
        ]

        if needs_path:
            command_list += [
                "--webhook-path",
                WEBHOOK_COMMAND_PATH_PLACEHOLDER,
            ]

        if needs_port_number:
            command_list += [
                "--webhook-port-number",
                WEBHOOK_COMMAND_PORT_PLACEHOLDER,
            ]

        routes_map[route_name]["command"] = command_list

    return routes_map
