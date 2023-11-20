import os

from addons.app.AppAddonManager import AppAddonManager

from addons.app.const.app import APP_DIR_APP_DATA
from src.decorator.option import option
from addons.app.decorator.app_command import app_command
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.Kernel import Kernel

@app_command(help="Create env variable pointing to files regarding environment extension")
@option('--dir', '-d', type=str, required=True, help="Argument")
def app__config__bind_files(kernel: 'Kernel', app_dir: str, dir: str):
    sub_dir_full = os.path.join(app_dir, APP_DIR_APP_DATA, dir)
    section_files = os.listdir(sub_dir_full)
    names_processed = []
    output = {}

    manager: AppAddonManager = kernel.addons['app']
    env = manager.get_runtime_config('env')

    for file in section_files:
        split = file.split('.')
        base_name = split[0]
        conf_var_name_list = split.copy()
        is_env = False

        # Check if there are more than two pieces in the file name
        if len(split) > 2:
            is_env = True
            if split[1] == env:
                # Remove env name
                conf_var_name_list = [split[0], split[2]]
            else:
                # This is an unexpected.name.ext; set conf_var_name to None
                conf_var_name_list = None

        # One execution only by base name,
        # Search for file variations inside it.
        # Allow to write the same variable two times if env file is found after the generic one.
        if conf_var_name_list and (base_name not in names_processed or is_env):
            # Save as found
            names_processed.append(base_name)
            # Insert the folder name (dir) into the second position
            conf_var_name_list.insert(1, dir)
            # Convert all elements to upper case and prepend 'CONF_'
            conf_var_name = '_'.join([element.lower() for element in conf_var_name_list])

            # Full path of the file
            file_path = os.path.realpath(os.path.join(sub_dir_full, file))

            # Save config
            manager.set_runtime_config(
                'bind.' + conf_var_name,
                file_path
            )

            output[conf_var_name] = file_path

    return output
