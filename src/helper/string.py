import re


def to_snake_case(text: str) -> str:
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


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


def text_truncate(text: str, max_width: int, indent: int = 0) -> str:
    lines = []
    for i in range(0, len(text), max_width):
        lines.append((" " * indent) + text[i:i + max_width])
    return "\n".join(lines)


def text_center(text: str, width: int) -> str:
    lines = text.split('\n')
    return '\n'.join(line.center(width) for line in lines)


def trim_leading(text: str, leading_text: str) -> str:
    if text.startswith(leading_text):
        return text[len(leading_text):]
    else:
        return text
