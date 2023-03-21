import re


def camel_to_snake_case(text: str) -> str:
    return re.sub(r'(?<!^)(?=[A-Z])', '_', text).lower()

def format_ignore_missing(string, substitutions):
    pattern = r'{(\w+)}'

    def replace(match):
        key = match.group(1)
        return substitutions.get(key, match.group(0))

    return re.sub(pattern, replace, string)
