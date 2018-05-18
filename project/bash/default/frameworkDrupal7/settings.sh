#!/usr/bin/env bash

frameworkDrupal7SettingsArgs() {
 _ARGUMENTS=(
   [0]='dir d "Root directory of drupal7" true'
 )
}

# Variables are stored globally like
# MYSQL_DB_USER,
# MYSQL_DB_XXX, etc.
frameworkDrupal7Settings() {
  eval $(php "${WEX_DIR_ROOT}php/drupal7SettingsToBash.php" ${DIR});
}
