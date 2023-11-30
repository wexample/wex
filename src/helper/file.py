import grp
import os
import pwd
import shutil
from typing import IO, Any, Dict, List, Optional


def file_list_subdirectories(path: str) -> List[str]:
    subdirectories = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path) and not item.startswith("."):
            subdirectories.append(os.path.basename(item_path))

    subdirectories.sort()

    return subdirectories


def file_set_user_or_sudo_user_owner(file: str) -> None:
    from src.helper.user import get_user_or_sudo_user

    sudo_user = get_user_or_sudo_user()
    if sudo_user is not None:
        file_set_owner(file, sudo_user)


def file_set_owner(
    file_path: str, username: Optional[str] = None, group: Optional[str] = None
) -> None:
    from src.helper.user import get_gid_from_group_name, get_user_or_sudo_user

    if username is None:
        username = get_user_or_sudo_user()

    # Get UID and GID of the user
    uid = pwd.getpwnam(username).pw_uid
    gid = get_gid_from_group_name(group) if group else pwd.getpwnam(username).pw_gid

    os.chown(file_path, uid, gid)


def file_set_owner_for_path_and_ancestors(
    base_path: str, sub_path: str, owner: str, group: Optional[str] = None
) -> None:
    # Get the UID and GID
    uid = pwd.getpwnam(owner).pw_uid

    if group:
        gid = grp.getgrnam(group).gr_gid
    else:
        gid = pwd.getpwnam(owner).pw_gid

    # Compute the full path
    full_path = os.path.join(base_path, sub_path)

    # Change the ownership of the full path
    os.chown(full_path, uid, gid)

    current_path = base_path
    # Split sub_path into segments and loop through them
    for segment in sub_path.strip(os.sep).split(os.sep):
        current_path = os.path.join(current_path, segment)
        os.chown(current_path, uid, gid)


def file_create_from_template(
    template_path: str, dest_path: str, parameters: Dict[str, str]
) -> None:
    with open(template_path, "r") as template_file:
        template_content = template_file.read()

    formatted_content = template_content.format(**parameters)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Replace the TO DOs, to prevent IDE warnings.
    formatted_content = formatted_content.replace("O/DO", "ODO")

    with open(dest_path, "w") as output_file:
        output_file.write(formatted_content)

    file_set_user_or_sudo_user_owner(dest_path)


def file_merge(src: str, dest: str) -> None:
    with open(src, "r") as src_file, open(dest, "a") as dest_file:
        dest_file.write(os.linesep)
        shutil.copyfileobj(src_file, dest_file)


def file_remove_duplicated_lines(file: str) -> None:
    with open(file, "r") as f:
        lines = f.readlines()

    filtered = []
    for line in lines:
        if line.strip() == "" or line not in filtered:
            filtered.append(line)

    with open(file, "w") as f:
        f.writelines(filtered)


def file_merge_new_lines(src: str, dest: str) -> None:
    file_merge(src, dest)
    file_remove_duplicated_lines(dest)


def file_create_directories_and_copy(path_from: str, path_to: str) -> None:
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(path_to), exist_ok=True)
    # Copy the file
    shutil.copy2(path_from, path_to)


def file_create_parent_dir(path: str) -> str:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path


def file_create_parent_and_touch(
    path: str,
    content: Optional[str] = None,
    default: Optional[str] = None,
    mode: str = "a",
) -> Optional[IO[Any]]:
    if os.path.exists(path):
        if content is not None:
            with open(path, mode) as file:
                file.write(content)

                file_set_owner(path)
                return file
        return None

    # Create all directories in the path
    file_create_parent_dir(path)

    # Create and close the file
    with open(path, mode) as file:
        if default or content:
            file.write(default or content)

            file_set_owner(path)
            return file
    return None


def file_write_dict_to_config(
    dictionary: Dict[str, bool | str], target_path: str
) -> None:
    output_lines = []
    for key, value in dictionary.items():
        # If the key starts with '#', write it as-is without the value
        if key.startswith("#"):
            output_lines.append(key)
        else:
            output_lines.append(f"{key.upper()}={str(value)}")

    output = os.linesep.join(output_lines)

    with open(target_path, "w") as f:
        f.write(output)


def file_set_dict_item_by_path(
    data: Dict[str, Any], key: str, value: Any, replace: bool = True
) -> None:
    keys = key.split(".")
    for k in keys[:-1]:
        data = data.setdefault(k, {})

    if not replace and keys[-1] in data:
        return

    data[keys[-1]] = value


def file_remove_dict_item_by_path(data: Dict[str, Any], key: str) -> None:
    keys = key.split(".")
    for k in keys[:-1]:
        if k not in data or not isinstance(data[k], dict):
            return
        data = data[k]

    data.pop(keys[-1], None)


def file_remove_file_if_exists(file: str) -> None:
    if os.path.isfile(file) or os.path.islink(file):
        os.remove(file)


def file_get_human_readable_size(size: float, decimal_places: int = 2) -> str:
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024.0:
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"


def file_get_owner(file_path: str) -> str:
    # Get the file stat object
    file_stat = os.stat(file_path)

    # Get the file owner UID
    uid = file_stat.st_uid

    # Get the owner's username
    owner_info = pwd.getpwuid(uid)
    return owner_info.pw_name


def file_get_group(file_path: str) -> str:
    # Get the file stat object
    file_stat = os.stat(file_path)

    # Get the file group GID
    gid = file_stat.st_gid

    # Get the group's name
    group_info = grp.getgrgid(gid)
    return group_info.gr_name


def file_build_date_time_name() -> str:
    from datetime import datetime

    return datetime.now().strftime("%Y-%m-%dT%H-%M-%S")


def file_delete_file_or_dir(path: str) -> None:
    if os.path.isdir(path):
        shutil.rmtree(path)
    else:
        os.remove(path)


def file_env_to_dict(env_path: str) -> Dict[str, str]:
    env_dict: Dict[str, str] = {}

    with open(env_path, "r") as f:
        for line in f.readlines():
            line = line.strip()

            if line.startswith("#") or not line:
                continue

            key, value = line.split("=", 1)
            env_dict[key] = value

    return env_dict


def file_read(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def file_write(file_path: str, content: str) -> None:
    with open(file_path, "w") as f:
        f.write(content)

def file_search(dir: str, pattern: str, recursive: bool = True) -> List[str]:
    matched_files = []

    if recursive:
        for root, dirs, files in os.walk(dir):
            for file in files:
                if file.endswith(pattern):
                    file_path = os.path.join(root, file)
                    matched_files.append(file_path)
    else:
        for file in os.listdir(dir):
            if file.endswith(pattern):
                file_path = os.path.join(dir, file)
                matched_files.append(file_path)

    return matched_files