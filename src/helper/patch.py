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
