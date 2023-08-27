import click

import os


@click.command()
@click.pass_obj
def maria_10__config__write_post(kernel):
    kernel.log("Maria : creating my.cnf file")

    config = kernel.addons['app']['config']
    # Create connexion file info
    my_conf_path = os.path.join(config['context']['dir_wex'], 'my.cnf')

    # Create or overwrite the file
    with open(my_conf_path, "w") as file:
        file.write('[client]\n')
        file.write(f'user = "{config["maria-10"]["user"]}"\n')
        file.write(f'password = "{config["maria-10"]["password"]}"\n')
