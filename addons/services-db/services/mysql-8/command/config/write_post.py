import click

import os


@click.command()
@click.pass_obj
def mysql_8__config__write_post(kernel):
    kernel.log("Maria : creating my.cnf file")

    config = kernel.addons['app']['config_build']

    # Create connexion file info
    my_conf_path = os.path.join(config['context']['dir_wex'], 'my.cnf')

    # Create or overwrite the file
    with open(my_conf_path, "w") as file:
        file.write('[client]\n')
        file.write(f'user = "{config["mysql-8"]["user"]}"\n')
        file.write(f'password = "{config["mysql-8"]["password"]}"\n')
