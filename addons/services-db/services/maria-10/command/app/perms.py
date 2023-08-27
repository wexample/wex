import click

import os


@click.command()
@click.pass_obj
def maria_10__app__perms(kernel):
    kernel.log("Maria : setting permissions my.cnf")

    config = kernel.addons['app']['config']
    # Create connexion file info
    my_conf_path = os.path.join(config['context']['dir_wex'], 'my.cnf')

    # Setting file permissions
    os.chmod(my_conf_path, 0o755)
    os.chmod(my_conf_path, 0o644)
