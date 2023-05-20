import re


def to_snake_case(text: str) -> str:
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
    s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    return re.sub('[_\\W]+', '_', s2)


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
