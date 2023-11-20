import os
import shutil
import git


def git_get_or_create_repo(path: str) -> git.Repo:
    try:
        return git.Repo(path)
    except git.InvalidGitRepositoryError:
        return git.Repo.init(path)


def git_move_or_file_move(repo: git.Repo, src: str, target: str) -> None:
    # Append git base dir.
    src = os.path.join(repo.working_tree_dir, src)
    target = os.path.join(repo.working_tree_dir, target)

    try:
        repo.git.mv(src, target)
    except git.GitCommandError:
        shutil.move(src, target)
