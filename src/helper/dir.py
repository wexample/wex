import os
import shutil
from typing import Any

from src.const.types import AnyCallable


def dir_execute_in_workdir(target_dir: str, callback: AnyCallable) -> Any:
    original_dir = os.getcwd()
    os.chdir(target_dir)
    response = callback()
    os.chdir(original_dir)

    return response


def dir_empty_dir(dir_path: str) -> None:
    # Iterate over each item in the directory
    for item_name in os.listdir(dir_path):
        # Construct the full path to the item
        item_path = os.path.join(dir_path, item_name)
        if os.path.isfile(item_path) or os.path.islink(item_path):
            os.remove(item_path)  # Remove the file or link
        elif os.path.isdir(item_path):
            # Recursively remove the directory
            shutil.rmtree(item_path)


def dir_set_permissions_recursively(
    path: str, mode: int, follow_symlinks: bool = True
) -> None:
    """
    Set permissions recursively for a given directory or file.

    :param path: Path to the directory or file.
    :param mode: Permission mode to set (e.g., 0o755).
    :param follow_symlinks: If False, symbolic links will not have their permissions changed.
    """
    # Change permissions for the current path
    try:
        if os.path.islink(path) and not follow_symlinks:
            # Optionally skip changing permissions of the symlink itself
            pass
        else:
            os.chmod(path, mode, follow_symlinks=follow_symlinks)
    except FileNotFoundError:
        pass

    # If the path is a directory (and not a symlink if follow_symlinks is False),
    # loop through its contents and call the function recursively
    if os.path.isdir(path) and (follow_symlinks or not os.path.islink(path)):
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            dir_set_permissions_recursively(item_path, mode, follow_symlinks)
