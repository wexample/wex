import re
from urllib.parse import urlparse, parse_qs

ALLOWED_ROUTES = {
    'status': r'^/status$',
    'webhook': r'^/webhook/([a-zA-Z0-9_\-]+)/([a-zA-Z0-9_\-]+)$',
}

# Added an explicit whitelist for query parameters
ALLOWED_QUERY_CHARS = re.compile(r'^[a-zA-Z0-9_\-=&]+$')


def get_route_name(url: str):
    parsed_url = urlparse(url)
    path = parsed_url.path

    for route_name, pattern in ALLOWED_ROUTES.items():
        if re.match(pattern, path):
            return route_name
    return None


def get_route_info(url: str):
    route_name = get_route_name(url)
    if route_name:
        parsed_url = urlparse(url)
        path = parsed_url.path
        query = parse_qs(parsed_url.query)
        pattern = ALLOWED_ROUTES[route_name]
        match = re.match(pattern, path)
        return {
            'path': route_name,
            'match': match.groups(),
            'query': query
        }


def is_allowed_route(url: str) -> bool:
    route_info = get_route_info(url)
    if route_info:
        # Validate the query string to contain only allowed characters
        for key, values in route_info['query'].items():
            for value in values:
                if not ALLOWED_QUERY_CHARS.fullmatch(value):
                    return False
        return True
    return False
