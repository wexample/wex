import yaml

from src.helper.dict import merge_dicts


def merge_docker_compose_files(src, dest):
    # Load both files as Python objects
    with open(src, 'r') as f:
        data1 = yaml.safe_load(f)
    with open(dest, 'r') as f:
        data2 = yaml.safe_load(f) or {}

    # Recursively merge the two objects
    merged_data = merge_dicts(data1, data2)

    # Write the merged data to a new file
    with open(dest, 'w') as f:
        yaml.dump(merged_data, f)

