import re
from typing import Dict, Any, Optional
from urllib.parse import urlparse, parse_qs

# Added an explicit whitelist for query parameters
ALLOWED_QUERY_CHARS = re.compile(r'^[a-zA-Z0-9_\-=&]+$')


def get_route_name(url: str, routes: Dict[str, Any]) -> Optional[str]:
    parsed_url = urlparse(url)
    path = parsed_url.path

    for route_name, config in routes.items():
        if re.match(config['pattern'], path):
            return route_name
    return None


def get_route_info(url: str, routes: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    route_name = get_route_name(url, routes)
    if route_name:
        parsed_url = urlparse(url)
        path = parsed_url.path
        query = parse_qs(parsed_url.query)
        route = routes[route_name]
        pattern = route['pattern']
        match = re.match(pattern, path)
        return {
            'async': route['async'],
            'name': route_name,
            'match': match.groups() if match else None,
            'query': query,
        }
    return None


def is_allowed_route(url: str, routes: Dict[str, Any]) -> bool:
    route_info = get_route_info(url, routes)
    if route_info:
        # Validate the query string to contain only allowed characters
        for key, values in route_info['query'].items():
            for value in values:
                if not ALLOWED_QUERY_CHARS.fullmatch(value):
                    return False
        return True
    return False
