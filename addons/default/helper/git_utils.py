import os
import shutil

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
    mode = os.stat(path).st_mode
    # Get only the lower 3 octal digits bit fields
    mode &= 0o777
    octal_permissions = oct(mode)[-3:]
    return f"100{octal_permissions}"
