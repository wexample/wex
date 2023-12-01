import re
from typing import Any
from urllib.parse import parse_qs, urlparse
from typing import TypedDict, Optional, Dict

from app.typing.webhook import WebhookListenerRoutesMap

# Added an explicit whitelist for query parameters
ALLOWED_QUERY_CHARS = re.compile(r"^[a-zA-Z0-9_\-=&]+$")


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
    match: re.Match
    query: Dict[str, list]


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
            match=match,
            query=query,
        )
    return None


def routing_is_allowed_route(url: str, routes: WebhookListenerRoutesMap) -> bool:
    route_info = routing_get_route_info(url, routes)
    if route_info:
        # Validate the query string to contain only allowed characters
        for key, values in route_info["query"].items():
            for value in values:
                if not ALLOWED_QUERY_CHARS.fullmatch(value):
                    return False
        return True
    return False
