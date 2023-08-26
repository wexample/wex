from yaml import SafeLoader

import json
import os
import shutil
import pwd
import grp
import yaml

from src.helper.system import get_user_or_sudo_user


def list_subdirectories(path: str) -> []:
    subdirectories = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path) and not item.startswith('.'):
            subdirectories.append(os.path.basename(item_path))

    subdirectories.sort()

    return subdirectories


def set_user_or_sudo_user_owner(file):
    sudo_user = get_user_or_sudo_user()
    if sudo_user is not None:
        set_owner(file, sudo_user)


def set_owner(file, username):
    # Get UID and GID of the sudo_user
    uid = pwd.getpwnam(username).pw_uid
    gid = grp.getgrnam(username).gr_gid

    # Change the ownership of the file to username:username
    os.chown(file, uid, gid)


def set_owner_recursive(base_path: str, sub_path: str, owner: str, group: str = None):
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


def create_directories_and_file(path: str, content: str = None) -> None:
    if os.path.exists(path):
        if content is not None:
            with open(path, 'w') as file:
                file.write(content)
        return

    # Create all directories in the path
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # Create and close the file
    with open(path, 'w') as file:
        if content:
            file.write(content)


def write_dict_to_config(dict, dest: str):
    with open(dest, 'w') as f:
        for key, value in dict.items():
            f.write(f"{key.upper()}={str(value).lower()}\n")


def get_yml_file_item(file_path: str, key: str, default=None):
    if os.path.exists(file_path):
        # Load the JSON file
        with open(file_path, 'r') as f:
            data = yaml.load(f, Loader=SafeLoader)

        return get_dict_item_by_path(data, key, default)
    return default


def set_json_file_item(file_path: str, key: str, value):
    if not os.path.exists(file_path):
        return

    with open(file_path, 'r') as f:
        data = json.load(f)

    keys = key.split('.')
    _set_json_file_item(data, keys, value)

    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)


def _set_json_file_item(dic, keys, value):
    key = keys.pop(0)
    if keys:
        if key not in dic:
            dic[key] = {}
        _set_json_file_item(dic[key], keys, value)
    else:
        dic[key] = value


def get_dict_item_by_path(data: dict, key: str, default = None):
    # Split the key into its individual parts
    keys = key.split('.')

    # Traverse the data dictionary using the key parts
    for k in keys:
        if k in data:
            data = data[k]
        else:
            return default

    return data


def yaml_load_or_default(file, default=None):
    if default is None:
        default = {}
    try:
        with open(file) as f:
            return yaml.load(f, SafeLoader)
    except FileNotFoundError:
        return default


def remove_file_if_exists(file: str):
    if os.path.isfile(file):
        os.remove(file)
