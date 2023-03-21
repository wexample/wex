import re


def to_snake_case(text: str) -> str:
    return re.sub(
        r'(?<!^)(?=[A-Z])',
        '_',
        text.replace('-', '_')
    ).lower()


def to_kebab_case(text: str) -> str:
    """
    Convert text to kebab case, converting spaces and underscores to dashes.
    """
    return re.sub(
        r'[_\s]+', '-',
        re.sub(r'([a-z])([A-Z])', r'\1-\2', text)
    ).lower()


def format_ignore_missing(string, substitutions):
    pattern = r'{(\w+)}'

    def replace(match):
        key = match.group(1)
        return substitutions.get(key, match.group(0))

    return re.sub(pattern, replace, string)
