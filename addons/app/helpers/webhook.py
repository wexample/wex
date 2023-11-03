import re
from urllib.parse import urlparse, parse_qs

ALLOWED_PATHS = {
    'status': r'^/status$',
    'webhook': r'^/webhook/([a-zA-Z_\-]+)/([a-zA-Z_\-]+)$',
}


def is_allowed_path(url: str):
    parsed_url = urlparse(url)
    path = parsed_url.path
    query = parse_qs(parsed_url.query)

    for valid_path, pattern in ALLOWED_PATHS.items():
        match = re.match(pattern, path)
        if match:
            return {
                'path': valid_path,
                'match': match.groups(),
                'query': query
            }

    return None
