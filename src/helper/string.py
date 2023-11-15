import re
import shutil


def to_snake_case(text: str) -> str:
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
    s2 = re.sub('([a-z])([A-Z])', r'\1_\2', s1).lower()
    s3 = re.sub('([0-9])([A-Z])', r'\1\2', s2)
    return re.sub('[\W]+', '_', s3)


def to_kebab_case(text: str) -> str:
    """
    Convert text to kebab case, converting spaces and underscores to dashes.
    """
    return re.sub(
        r'[_\s]+', '-',
        re.sub(r'([a-z])([A-Z])', r'\1-\2', text)
    ).lower()


def to_camel_case(text: str) -> str:
    s1 = to_snake_case(text)
    return re.sub(r'_([a-z])', lambda x: x.group(1).upper(), s1)


def to_pascal_case(text: str) -> str:
    # Use to_camel_case to convert to camelCase first
    camel_case = to_camel_case(text)
    # Convert the first letter to uppercase to get PascalCase
    return camel_case[0].upper() + camel_case[1:]


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


def count_lines_needed(message: str) -> int:
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


def replace_variables(text: str, variables: dict) -> str:
    # Pattern to match $VAR and ${VAR}
    pattern = re.compile(r'\$\{?([A-Z_]+)\}?')

    # Replacement function
    def repl(match):
        return variables.get(
            match.group(1).upper(),
            match.group(0))

    # Substitute using the replacement function
    return pattern.sub(repl, text)
