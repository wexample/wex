import os
import shutil

from src.const.types import AnyCallable


def dir_execute_in_workdir(target_dir: str, callback: AnyCallable) -> None:
    original_dir = os.getcwd()
    os.chdir(target_dir)
    callback()
    os.chdir(original_dir)


def dir_empty_dir(dir_path) -> None:
    # Iterate over each item in the directory
    for item_name in os.listdir(dir_path):
        # Construct the full path to the item
        item_path = os.path.join(dir_path, item_name)
        if os.path.isfile(item_path) or os.path.islink(item_path):
            os.remove(item_path)  # Remove the file or link
        elif os.path.isdir(item_path):
            # Recursively remove the directory
            shutil.rmtree(item_path)
