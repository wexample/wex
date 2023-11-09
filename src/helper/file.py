from yaml import SafeLoader

import os
import shutil
import pwd
import grp
import yaml


def list_subdirectories(path: str) -> []:
    subdirectories = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path) and not item.startswith('.'):
            subdirectories.append(os.path.basename(item_path))

    subdirectories.sort()

    return subdirectories


def set_user_or_sudo_user_owner(file):
    from src.helper.system import get_user_or_sudo_user

    sudo_user = get_user_or_sudo_user()
    if sudo_user is not None:
        set_owner(file, sudo_user)


def set_owner(file: str, username: str | None = None, group: str | None = None):
    if not username:
        from src.helper.system import get_user_or_sudo_user
        username = get_user_or_sudo_user()

    # Get UID and GID of the sudo_user
    uid = pwd.getpwnam(username).pw_uid

    if group:
        from helper.system import get_gid_from_group_name
        gid = get_gid_from_group_name(username)
    else:
        gid = grp.getgrnam(username).gr_gid

    # Change the ownership of the file to username:username
    os.chown(file, uid, gid)


def set_owner_for_path_and_ancestors(base_path: str, sub_path: str, owner: str, group: str = None):
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


def create_from_template(template_path, dest_path, parameters):
    with open(template_path, 'r') as template_file:
        template_content = template_file.read()

    formatted_content = template_content.format(
        **parameters
    )

    os.makedirs(
        os.path.dirname(dest_path),
        exist_ok=True
    )

    # Replace the TO DOs, to prevent IDE warnings.
    formatted_content = formatted_content.replace("O/DO", "ODO")

    with open(dest_path, 'w') as output_file:
        output_file.write(formatted_content)

    set_user_or_sudo_user_owner(dest_path)


def merge_files(src: str, dest: str) -> None:
    with open(src, 'r') as src_file, open(dest, 'a') as dest_file:
        dest_file.write('\n')
        shutil.copyfileobj(src_file, dest_file)


def remove_duplicated_lines(file: str) -> None:
    with open(file, 'r') as f:
        lines = f.readlines()

    filtered = []
    for line in lines:
        if line.strip() == "" or line not in filtered:
            filtered.append(line)

    with open(file, 'w') as f:
        f.writelines(filtered)


def merge_new_lines(src: str, dest: str) -> None:
    merge_files(src, dest)
    remove_duplicated_lines(dest)


def create_directories_and_copy(path_from: str, path_to: str) -> None:
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(path_to), exist_ok=True)
    # Copy the file
    shutil.copy2(path_from, path_to)


def create_file_path(path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path


def create_directories_and_file(
        path: str,
        content: str = None,
        default: str = None,
        mode: str = 'a'):
    if os.path.exists(path):
        if content is not None:
            with open(path, mode) as file:
                file.write(content)

                set_owner(path)
                return file
        return

    # Create all directories in the path
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # Create and close the file
    with open(path, mode) as file:
        if default or content:
            file.write(default or content)

            set_owner(path)
            return file
    return


def write_dict_to_config(dict: dict, dest: str):
    output_lines = []
    for key, value in dict.items():
        # If the key starts with '#', write it as-is without the value
        if key.startswith("#"):
            output_lines.append(key)
        else:
            output_lines.append(f"{key.upper()}={str(value)}")

    output = "\n".join(output_lines)

    with open(dest, 'w') as f:
        f.write(output)


def set_dict_item_by_path(data: dict, key: str, value, replace: bool = True):
    keys = key.split('.')
    for k in keys[:-1]:
        data = data.setdefault(k, {})

    if not replace and keys[-1] in data:
        return

    data[keys[-1]] = value


def yaml_load_or_default(file, default=None):
    if default is None:
        default = {}
    try:
        with open(file) as f:
            return yaml.load(f, SafeLoader)
    except FileNotFoundError:
        return default


def remove_file_if_exists(file: str):
    if os.path.isfile(file) or os.path.islink(file):
        os.remove(file)


def human_readable_size(size, decimal_places=2):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"


def get_file_owner(file_path) -> str:
    # Get the file stat object
    file_stat = os.stat(file_path)

    # Get the file owner UID
    uid = file_stat.st_uid

    # Get the owner's username
    owner_info = pwd.getpwuid(uid)
    return owner_info.pw_name


def get_file_group(file_path) -> str:
    # Get the file stat object
    file_stat = os.stat(file_path)

    # Get the file group GID
    gid = file_stat.st_gid

    # Get the group's name
    group_info = grp.getgrgid(gid)
    return group_info.gr_name


def date_time_file_name():
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%dT%H-%M-%S")


def delete_file_or_dir(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    else:
        os.remove(path)


def env_to_dict(env_path: str) -> dict:
    env_dict: dict = {}

    with open(env_path, 'r') as f:
        for line in f.readlines():
            line = line.strip()

            if line.startswith("#") or not line:
                continue

            key, value = line.split("=", 1)
            env_dict[key] = value

    return env_dict


def file_read(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
