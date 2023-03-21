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

    unique_lines = list(set(lines))

    with open(file, 'w') as f:
        f.writelines(unique_lines)


def merge_gitignore(src: str, dest: str) -> None:
    merge_files(src, dest)
    remove_duplicated_lines(dest)
