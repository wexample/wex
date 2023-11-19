import os
import re
import shutil
from typing import Dict


def string_to_snake_case(text: str) -> str:
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
    s2 = re.sub('([a-z])([A-Z])', r'\1_\2', s1).lower()
    s3 = re.sub('([0-9])([A-Z])', r'\1\2', s2)
    return re.sub('\W+', '_', s3)


def string_to_kebab_case(text: str) -> str:
    """
    Convert text to kebab case, converting spaces and underscores to dashes.
    """
    return re.sub(
        r'[_\s]+', '-',
        re.sub(r'([a-z])([A-Z])', r'\1-\2', text)
    ).lower()


def string_to_camel_case(text: str) -> str:
    s1 = string_to_snake_case(text)
    return re.sub(r'_([a-z])', lambda x: x.group(1).upper(), s1)


def string_to_pascal_case(text: str) -> str:
    # Use to_camel_case to convert to camelCase first
    camel_case = string_to_camel_case(text)
    # Convert the first letter to uppercase to get PascalCase
    return camel_case[0].upper() + camel_case[1:]


def string_format_ignore_missing(value: str, substitutions: Dict[str, str]) -> str:
    pattern = r'{(\w+)}'

    def replace(match: re.Match[str]) -> str:
        key = match.group(1)
        return substitutions.get(key, match.group(0))

    return re.sub(pattern, replace, value)


def string_truncate(text: str, max_width: int, indent: int = 0) -> str:
    lines = []
    for i in range(0, len(text), max_width):
        lines.append((" " * indent) + text[i:i + max_width])
    return os.linesep.join(lines)


def string_multiline_center(text: str, width: int) -> str:
    lines = text.split(os.linesep)
    return os.linesep.join(line.center(width) for line in lines)


def string_trim_leading(text: str, leading_text: str) -> str:
    if text.startswith(leading_text):
        return text[len(leading_text):]
    else:
        return text


def string_count_lines_needed(message: str) -> int:
    """Calculate the number of lines needed to display a message in the terminal."""
    # Get terminal size
    terminal_width, _ = shutil.get_terminal_size()

    if terminal_width < 1:
        return 1

    # Count invisible characters (ANSI escape sequences)
    invisible_chars = 0
    in_escape_sequence = False
    for char in message:
        if char == '\033':
            in_escape_sequence = True
        if in_escape_sequence:
            invisible_chars += 1
        if char == 'm':
            in_escape_sequence = False

    # Calculate the visible length of the message
    visible_length = len(message) - invisible_chars

    # Calculate the number of lines needed, equivalent to math.ceil(visible_length / terminal_width)
    lines_needed = -(-visible_length // terminal_width)

    return lines_needed


def string_replace_multiple(text: str, variables: Dict[str, str]) -> str:
    # Pattern to match $VAR and ${VAR}
    pattern = re.compile(r'\$\{?([A-Z_]+)\}?')

    # Replacement function
    def repl(match: re.Match[str]) -> str:
        return variables.get(
            match.group(1).upper(),
            match.group(0))

    # Substitute using the replacement function
    return pattern.sub(repl, text)
