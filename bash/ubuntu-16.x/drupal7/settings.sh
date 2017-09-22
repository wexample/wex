#!/usr/bin/env bash

drupal7SettingsArgs() {
 _ARGUMENTS=(
   [0]='dir d "Root directory of drupal7" false'
 )
}

# Variables are stored globally like
# WEBSITE_SETTINGS_USERNAME,
# WEBSITE_SETTINGS_XXX, etc.
drupal7Settings() {
  eval $(php "${WEX_DIR_BASH_UBUNTU16}../../php/drupal7SettingsToBash.php" ${DIR});
}
