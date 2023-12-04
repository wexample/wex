import os

from src.const.types import AnyCallable


def dir_execute_in_workdir(target_dir: str, callback: AnyCallable) -> None:
    original_dir = os.getcwd()
    os.chdir(target_dir)
    callback()
    os.chdir(original_dir)
