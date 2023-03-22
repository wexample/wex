import json
import os
import shutil


def list_subdirectories(path: str) -> []:
    subdirectories = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path) and not item.startswith('.'):
            subdirectories.append(os.path.basename(item_path))

    subdirectories.sort()

    return subdirectories


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


def create_directories_and_file(path: str) -> None:
    if os.path.exists(path):
        return

    # Create all directories in the path
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # Create and close the file
    with open(path, 'w') as _:
        pass


def write_dict_to_config(dict, dest: str):
    with open(dest, 'w') as f:
        for key, value in dict.items():
            f.write(f"{key.upper()}={str(value).lower()}\n")


def get_json_file_item(file_path: str, key: str):
    if os.path.exists(file_path):
        # Load the JSON file
        with open(file_path, 'r') as f:
            data = json.load(f)

        return get_json_item(data, key)
    return None


def get_json_item(json_data, key: str):
    # Split the key into its individual parts
    keys = key.split('.')

    # Traverse the data dictionary using the key parts
    for k in keys:
        if k in json_data:
            json_data = json_data[k]
        else:
            return None

    return json_data
