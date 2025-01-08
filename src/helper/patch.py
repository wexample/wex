from typing import List, Optional

import patch
from wexample_helpers.helpers.directory import directory_execute_inside


def patch_is_valid(text: str) -> bool:
    # Check hunt header
    if "@@" not in text:
        return False

    # Search for any + or - line
    lines = text.split("\n")
    for line in lines:
        if line.startswith("+") or line.startswith("-"):
            return True

    return False


def patch_apply_in_workdir(workdir: str, patch_set: patch.PatchSet) -> bool:
    def _patch_it():
        return patch_set.apply()

    return directory_execute_inside(workdir, _patch_it)


def extract_information(
    patch_content: str, prefix: str, default: Optional[str] = None
) -> Optional[str]:
    # Format the prefix to fit the expected pattern in patch content
    formatted_prefix = f"# {prefix}:"

    # Split the content into lines
    lines = patch_content.split("\n")

    # Look for the line starting with the specified formatted prefix
    for line in lines:
        if line.strip().startswith(formatted_prefix):
            # Extract and return the information after the prefix
            return line.strip()[len(formatted_prefix) :].strip()
    return default


def patch_clean(patch_content: str) -> str:
    # Split the content into lines
    lines = patch_content.split("\n")

    # Collect non-comment lines
    cleaned_lines = [line for line in lines if not line.strip().startswith("# ")]

    # Join the cleaned lines back into a single string
    return "\n".join(cleaned_lines).rstrip()


def patch_has_all_parts(file_content: str, patch_parts: List[List[str]]) -> bool:
    """
    Check if all groups of parts in patch_parts are contained in file_content in the given order.
    Each group must appear in the order provided within the group itself.

    Args:
    file_content (str): The full content of the file as a string.
    patch_parts (list with list of str): List of groups of file parts to be checked.

    Returns:
    bool: True if all groups and their parts are found in order in the file_content, False otherwise.
    """
    last_found_index = 0  # Starting index for the search

    for group in patch_parts:
        for part in group:
            # Find the current part in the file content, starting the search from the last found index
            current_index = file_content.find(part, last_found_index)

            if current_index == -1:
                # If current part is not found, return False
                return False
            else:
                # Update the last found index to the end of the current part
                last_found_index = current_index + len(part)

        # Update the search index to start after the last found part in this group
        # to ensure the next group starts after this group
        last_found_index = file_content.find(group[-1], last_found_index) + len(
            group[-1]
        )

    return True  # All groups and parts were found in order


def patch_find_line_of_first_subgroup(
    file_content: str, patch_parts: List[List[str]]
) -> int:
    """
    Find the line number of the first subgroup in patch_parts within the file_content.

    Args:
    file_content (str): The full content of the file as a string split into lines.
    patch_parts (list with list of str): List of groups of file parts to be checked.

    Returns:
    int: Line number where the first subgroup is found, or -1 if not found.
    """
    # Extract the first subgroup from the list, assuming there is at least one group and one subgroup
    first_subgroup = patch_parts[0][0] if patch_parts and patch_parts[0] else None
    if first_subgroup:
        lines = file_content.split("\n")  # Split the content into lines
        for index, line in enumerate(lines):
            if first_subgroup in line:
                return index + 1  # Return the line number (1-based index)
    return -1  # Return -1 if the part is not found or if no parts are provided


def patch_get_lines_by_type(patch_content: str, line_type: str) -> List[str]:
    """
    Generic function to return lines based on their starting character.

    Args:
    patch_content (str): The content of the patch file as a string.
    line_type (str): The character that lines must start with to be included.

    Returns:
    List[str]: A list of lines that start with the specified character.
    """
    lines = patch_content.split("\n")
    selected_lines = []
    for line in lines:
        if line.startswith(" ") or line.startswith(line_type) or line.strip() == "":
            # Remove the first char, " ", or "-", or "+"
            selected_lines.append(line[1:])
    return selected_lines


def patch_get_initial_lines(patch_content: str) -> List[str]:
    """
    Return lines which belong to the initial file (exclude the "+" adds) in a patch set.
    """
    return patch_get_lines_by_type(patch_content, "-")


def patch_get_applied_lines(patch_content: str) -> List[str]:
    """
    Return lines as they would appear after the patch is applied (include only the "+" adds).
    """
    return patch_get_lines_by_type(patch_content, "+")


def patch_create_hunk_header(file_content: str, patch_content: str) -> Optional[str]:
    patch_parts = patch_get_initial_parts(patch_content)

    if patch_has_all_parts(file_content, patch_parts):
        start_line = str(
            patch_find_line_of_first_subgroup(
                file_content=file_content, patch_parts=patch_parts
            )
        )

        hunk_header = ""
        hunk_header += (
            "-"
            + (start_line if file_content else "0")
            + ","
            + str(len(patch_get_initial_lines(patch_content)))
            + " "
        )
        hunk_header += (
            "+" + start_line + "," + str(len(patch_get_applied_lines(patch_content)))
        )

        return f"@@ {hunk_header} @@"

    return None


def patch_get_initial_parts(patch_content: str) -> List[List[str]]:
    """
    Extract contiguous groups of lines starting with ' ' or '-', ignoring lines starting with '+' or other characters.

    Args:
    patch_content (str): The content of the patch file as a string.

    Returns:
    List[List[str]]: A list of groups, each containing lines starting with ' ' or '-'.
    """
    lines = patch_content.split("\n")  # Split the content into individual lines
    result = []
    current_group = []

    for line in lines:
        if line.startswith(" ") or line.startswith("-"):
            # If the line starts with ' ' or '-', add it to the current group
            current_group.append(line[1:])
        elif current_group:
            # If a new line doesn't match and there is an existing group, save it and start a new group
            result.append(current_group)
            current_group = []

    # Add the last group if it's not empty
    if current_group:
        result.append(current_group)

    return result
