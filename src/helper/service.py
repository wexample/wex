import os


def get_service_dir(kernel, service: str) -> str:
    addon = kernel.registry['services'][service]['addon']

    return os.path.join(kernel.path['addons'], addon, 'services', service)


def service_get_inheritance_tree(kernel, service):
    # Initialize an empty list to store the inheritance tree
    inheritance_tree = []

    # Get the configuration of the given service
    service_config = kernel.registry['services'].get(service, {})

    # Check if the service has an 'extends' property
    parent_service = service_config.get('config', {}).get('extends')

    # If it does, recursively find its inheritance tree
    if parent_service:
        inheritance_tree.extend(service_get_inheritance_tree(kernel, parent_service))

    # Add the current service to the inheritance tree
    inheritance_tree.append(service)

    # Reverse the list to make the original service the first element
    inheritance_tree.reverse()

    return inheritance_tree
