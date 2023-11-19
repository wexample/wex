import os
import shutil
import git


def get_or_create_repo(path):
    try:
        return git.Repo(path)
    except git.InvalidGitRepositoryError:
        return git.Repo.init(path)


def file_move_or_git_move(repo: git.Repo, src: str, dest: str):
    # Append git base dir.
    src = os.path.join(repo.working_tree_dir, src)
    dest = os.path.join(repo.working_tree_dir, dest)

    try:
        repo.git.mv(src, dest)
    except git.GitCommandError:
        shutil.move(src, dest)
