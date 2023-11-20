import os
import shutil
import git


def git_get_or_create_repo(path: str) -> git.Repo:
    try:
        return git.Repo(path)
    except git.InvalidGitRepositoryError:
        return git.Repo.init(path)


def git_move_or_file_move(repo: git.Repo, src: str, target: str) -> None:
    repo_dir = repo.working_tree_dir

    if not isinstance(repo_dir, str):
        return

    # Append git base dir.
    src = os.path.join(repo_dir, src)
    target = os.path.join(repo_dir, target)

    try:
        repo.git.mv(src, target)
    except git.GitCommandError:
        shutil.move(src, target)
