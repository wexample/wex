#!/usr/bin/env bash

frameworkDrupal7SettingsArgs() {
 _ARGUMENTS=(
   [0]='dir d "Root directory of drupal7" true'
 )
}

# Variables are stored globally like
# SITE_DB_USER,
# SITE_DB_XXX, etc.
frameworkDrupal7Settings() {
  eval $(php "${WEX_DIR_ROOT}php/drupal7SettingsToBash.php" ${DIR});
}
