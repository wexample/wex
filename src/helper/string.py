import os
import random
import re
import shutil
import string
from typing import List, Mapping, Optional

from wexample_helpers.helpers.string import string_to_snake_case

from src.const.types import BasicInlineValue, StringsDict, StringsList, StringsMatch


def string_to_camel_case(text: str) -> str:
    s1 = string_to_snake_case(text)
    return re.sub(r"_([a-z])", lambda x: x.group(1).upper(), s1)


def string_to_pascal_case(text: str) -> str:
    # Use to_camel_case to convert to camelCase first
    camel_case = string_to_camel_case(text)
    # Convert the first letter to uppercase to get PascalCase
    return camel_case[0].upper() + camel_case[1:]


def string_format_ignore_missing(
    value: str, substitutions: Optional[StringsDict] = None
) -> str:
    pattern = r"{(\w+)}"
    substitutions = substitutions or {}

    def replace(match: StringsMatch) -> str:
        key = match.group(1)
        return substitutions.get(key, match.group(0))

    return re.sub(pattern, replace, value)


def string_truncate(text: str, max_width: int, indent: int = 0) -> str:
    lines = []
    for i in range(0, len(text), max_width):
        lines.append((" " * indent) + text[i : i + max_width])
    return os.linesep.join(lines)


def string_multiline_center(text: str, width: int) -> str:
    lines = text.split(os.linesep)
    return os.linesep.join(line.center(width) for line in lines)


def string_trim_leading(text: str, leading_text: str) -> str:
    if text.startswith(leading_text):
        return text[len(leading_text) :]
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
        if char == "\033":
            in_escape_sequence = True
        if in_escape_sequence:
            invisible_chars += 1
        if char == "m":
            in_escape_sequence = False

    # Calculate the visible length of the message
    visible_length = len(message) - invisible_chars

    # Calculate the number of lines needed, equivalent to math.ceil(visible_length / terminal_width)
    lines_needed = -(-visible_length // terminal_width)

    return lines_needed


def string_replace_multiple(
    text: str, variables: Mapping[str, BasicInlineValue]
) -> str:
    # Pattern to match $VAR and ${VAR}
    pattern = re.compile(r"\$\{?([A-Z_]+)\}?")

    # Replacement function
    def repl(match: StringsMatch) -> str:
        return str(variables.get(match.group(1).upper(), match.group(0)))

    # Substitute using the replacement function
    return pattern.sub(repl, text)


def string_random_password_secure(length: int = 64) -> str:
    """
    Creates a secure password that is at least 8 characters long and contains characters
    from at least three of the four following sets: Uppercase letters, Lowercase letters,
    Base 10 digits, and a reduced set of Symbols.
    """

    # Define character sets
    upper = string.ascii_uppercase  # Uppercase letters
    lower = string.ascii_lowercase  # Lowercase letters
    digits = string.digits  # Base 10 digits
    safe_symbols = "._-+"  # Reduced set of symbols

    # Combine all character sets into a list
    all_sets = [
        upper,
        upper,
        upper,
        lower,
        lower,
        lower,
        lower,
        lower,
        lower,
        lower,
        digits,
        digits,
        safe_symbols,
    ]
    random.shuffle(all_sets)  # Shuffle to ensure randomness

    count = 0
    password = ""
    sets_modulo = len(all_sets) - 1
    while count < length:
        password += random.choice(all_sets[count % sets_modulo])
        count += 1

    return password


def string_random_password(length: int = 64) -> str:
    """
    Creates a password using only alphanumerical character as it is easier to copy / paste.
    """
    characters = string.ascii_letters

    random_string = "".join(random.choice(characters) for _ in range(length))

    return random_string


def string_has_trailing_new_line(file_content: str) -> bool:
    return file_content.endswith("\n")


def string_add_lines_numbers(file_content: str) -> Optional[str]:
    file_content_lines = file_content.split(os.linesep)

    # Determine the number of digits in the largest line number for proper alignment
    max_line_number = len(file_content_lines)
    number_zone_spacing = len(str(max_line_number))

    # Initialize an empty string to accumulate the result
    formatted_content = ""
    for i, line in enumerate(
        file_content_lines, start=1
    ):  # Start counting lines from 1
        # Format each line with its line number, ensuring proper alignment
        # Strip the newline character from each line and add it back manually to avoid double newlines when joining
        line_number = f"{i:>{number_zone_spacing}} | {line.rstrip()}\n"
        formatted_content += line_number

    return formatted_content


def string_list_calculate_max_widths(array: StringsList) -> List[int]:
    """
    Calculate the maximum widths for each column based on the array.
    """
    if not array:  # If the array is empty, return an empty list
        return []

    # Find the row with the maximum number of columns
    num_columns = max(len(row) for row in array)

    # Initialize max widths with zeros for each column
    max_widths = [0] * num_columns

    for row in array:
        for i, cell in enumerate(row):
            # Update the max width for each column if current cell is larger
            max_widths[i] = max(max_widths[i], len(str(cell)))

    return max_widths


def string_list_longest_word(word_list: StringsList) -> int:
    if not word_list:  # list is empty
        return 0
    else:
        return max(len(word) for word in word_list)
