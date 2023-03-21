import os


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

    with open(dest_path, 'w') as output_file:
        output_file.write(formatted_content)
