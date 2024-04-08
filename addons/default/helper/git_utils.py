import os
import shutil
import stat

from git import GitCommandError, InvalidGitRepositoryError, Repo


def git_get_or_create_repo(path: str) -> Repo:
    try:
        return Repo(path)
    except InvalidGitRepositoryError:
        return Repo.init(path)


def git_move_or_file_move(repo: Repo, src: str, target: str) -> None:
    repo_dir = repo.working_tree_dir

    if not isinstance(repo_dir, str):
        return

    # Append git base dir.
    src = os.path.join(repo_dir, src)
    target = os.path.join(repo_dir, target)

    try:
        repo.git.mv(src, target)
    except GitCommandError:
        shutil.move(src, target)


def git_file_get_octal_mode(path: str) -> str:
    """
    Determine the Git mode of a file based on its current permissions.
    Returns:
    - A string representing the Git mode of the file ('100644' for non-executable,
      '100755' for executable, etc.).
    """
    # Retrieve the mode of the file (permissions)
    file_stats = os.stat(path)
    mode = file_stats.st_mode

    # Check if the file is executable by anyone (owner, group, others)
    if mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH):
        return "100755"  # File is executable
    else:
        return "100644"  # File is not executable
