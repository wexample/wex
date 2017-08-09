#!/usr/bin/env bash

# Variables are stored globally like
# WEX_DRUPAL_7_SETTINGS_USERNAME,
# WEX_DRUPAL_7_SETTINGS_XXX, etc.
drupal7Settings() {
  eval $(php "${WEX_DIR_ROOT}../../php/drupal7SettingsToBash.php" ${1});
}
