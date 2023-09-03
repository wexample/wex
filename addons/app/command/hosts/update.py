import click

from addons.app.decorator.app_location_optional import app_location_optional
from src.decorator.as_sudo import as_sudo
from src.core.Kernel import Kernel
from src.decorator.command import command

@command()
@as_sudo
@app_location_optional
def app__hosts__update(kernel: Kernel):
    hosts_path = '/etc/hosts'

    # TODO This behavior is inherited, maybe we can now redirect local requests to containers without modifying the host file

    # new_block_content = []
    # ip = kernel.run_function(
    #     docker__docker__ip
    # )
    #
    # for app_name, app_dir in kernel.addons['app']['proxy']['apps'].items():
    #     new_block_content.append(f'{app_name}\t{ip}')
    # new_block_content = '\n'.join(new_block_content)
    #
    # kernel.log(f'Updating {hosts_path}')
    #
    # with open(hosts_path, 'r') as f:
    #     hosts_content = f.read()
    #
    # # Remove old wex block
    # hosts_content = remove_wex_block(hosts_content)
    #
    # # Add the new wex block
    # hosts_content = add_wex_block(hosts_content, new_block_content)
    #
    # # Write the updated content back to the file
    # with open(hosts_path, 'w') as f:
    #     f.write(hosts_content)


def remove_wex_block(text):
    """
    Removes any text surrounded by "#[ wex ]#...#[ endwex ]#" in a given string variable.
    """
    lines = text.split("\n")
    new_lines = []
    in_wex_block = False

    for line in lines:
        if "#[ wex ]#" in line:
            in_wex_block = True
        elif "#[ endwex ]#" in line:
            in_wex_block = False
            continue

        if not in_wex_block:
            new_lines.append(line)

    return "\n".join(new_lines)


def add_wex_block(text, block_content):
    """
    Adds a text surrounded by "#[ wex ]#...#[ endwex ]#" in a given string variable.
    """
    return text + "\n#[ wex ]#\n" + block_content + "\n#[ endwex ]#\n"
