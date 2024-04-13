from typing import Optional, Tuple

import patch
from src.helper.dir import dir_execute_in_workdir


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

    return dir_execute_in_workdir(workdir, _patch_it)


def patch_extract_description_and_clean_patch(patch_content: str) -> Tuple[str, str]:
    # Split the content into lines
    lines = patch_content.split("\n")

    # Define the prefix to look for the description
    description_prefix = "# DESCRIPTION:"

    # Initialize variables
    description: Optional[str] = None
    cleaned_patch = []

    # Iterate over each line to find the description and exclude comment lines
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith(description_prefix):
            # Extract the description and mark as found
            description = stripped_line[len(description_prefix):].strip()
        elif not stripped_line.startswith("# "):
            # Include only lines that do not start with "# "
            cleaned_patch.append(line)

    # Prepare the return values
    cleaned_patch_content = "\n".join(cleaned_patch)

    # Return the description and the cleaned patch content
    return (description if description is not None else 'No description found'), cleaned_patch_content
